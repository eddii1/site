"""Compute word-to-word attention over the home page bio, for the hover arcs.

The site build has no Python or model, so run this by hand whenever src/data/bio.json changes. It writes
src/data/bio-attention.json, and the home page refuses to build if that file's text differs from the bio,
so the arcs can never go stale.

    python scripts/bio-attention.py           # write the JSON for LAYER/HEAD below
    python scripts/bio-attention.py --rank    # list the heads that best relate content words, to re-pick one

Needs torch and transformers. The model is BAAI/bge-m3 (an XLM-RoBERTa encoder, so attention is
bidirectional: a word can look at words after it, which is what a hover over a sentence should show).
"""

import json
import re
import sys
from pathlib import Path

import torch
from transformers import AutoModel, AutoTokenizer

MODEL = "BAAI/bge-m3"
# Picked with --rank, then by reading the arcs: this head links "built" to "product", "customers" to
# "paying", "RAG" to "document", "Milan" to "startup". Zero-indexed, as in the model's own tensors.
LAYER, HEAD = 11, 10
TOP_K = 3  # arcs per hovered word
MIN_SHARE = 0.08  # drop arcs below this share of the word's attention to content words

ROOT = Path(__file__).resolve().parent.parent
BIO = ROOT / "src" / "data" / "bio.json"
OUT = ROOT / "src" / "data" / "bio-attention.json"

# Function words: not hoverable and never an arc target. Their attention is mostly positional noise.
STOP = set("a an the and or of at in on to from its it i i'm was is that by for with up before".split())


def words_of(text):
    """(word, start, end) for each word; punctuation is never part of a word."""
    return [(m.group(), m.start(), m.end()) for m in re.finditer(r"[A-Za-z0-9][\w'’-]*", text)]


def word_attention(tok, model, text):
    """Attention between words for every layer and head: [layers, heads, words, words].

    A word split into several tokens gets the mean of its tokens' rows (where it looks) and the sum of
    the target's columns (how much is spent on that word). Special tokens and punctuation are dropped.
    """
    enc = tok(text, return_offsets_mapping=True, return_tensors="pt")
    offsets = enc.pop("offset_mapping")[0].tolist()
    with torch.no_grad():
        att = torch.stack(model(**enc, output_attentions=True).attentions)[:, 0]  # [L, H, T, T]
    words = words_of(text)
    member = torch.zeros(len(words), len(offsets))
    for t, (s, e) in enumerate(offsets):
        for k, (_, ws, we) in enumerate(words):
            if e > s and s < we and e > ws:
                member[k, t] = 1
                break
    rows = member / member.sum(1, keepdim=True)
    return words, torch.einsum("wt,lhts,vs->lhwv", rows, att, member)


def content_mask(words):
    return torch.tensor([w.lower() not in STOP for w, _, _ in words])


def rank(encoded):
    """Score heads: attention spent on other content words, that differs per word (not one sink
    every word stares at), and that reaches past the next word (not a positional head)."""
    L, H = encoded[0][1].shape[:2]
    scores = torch.zeros(L, H)
    for words, W in encoded:
        c = content_mask(words)
        idx = torch.arange(len(words))
        far = ((idx[:, None] - idx[c][None, :]).abs() > 1).float()
        M = W.clone()
        M[..., idx, idx] = 0
        M = M[..., c][..., c, :]
        mass = M.sum(-1)
        R = M / mass.unsqueeze(-1).clamp(min=1e-9)
        mean = R.mean(-2, keepdim=True)
        diverse = (R * (R.clamp(min=1e-9) / mean.clamp(min=1e-9)).log()).sum(-1)
        reach = (R * far[c]).sum(-1)
        scores += (mass * diverse * reach).mean(-1)
    for s, (l, h) in sorted(((scores[l, h].item(), (l, h)) for l in range(L) for h in range(H)), reverse=True)[:12]:
        print(f"layer {l:2d} head {h:2d}  {s:.3f}")


def main():
    paragraphs = json.loads(BIO.read_text())
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModel.from_pretrained(MODEL, attn_implementation="eager").eval()
    encoded = [word_attention(tok, model, text) for text in paragraphs]

    if "--rank" in sys.argv:
        rank(encoded)
        return

    out = {"model": MODEL, "layer": LAYER, "head": HEAD, "paragraphs": []}
    for text, (words, W) in zip(paragraphs, encoded):
        A = W[LAYER, HEAD]
        c = content_mask(words)
        arcs = []
        for i in range(len(words)):
            if not c[i]:
                arcs.append([])
                continue
            row = [(j, A[i, j].item()) for j in range(len(words)) if j != i and c[j]]
            total = sum(w for _, w in row) or 1.0
            row = sorted(((j, w / total) for j, w in row), key=lambda x: -x[1])[:TOP_K]
            arcs.append([[j, round(w, 3)] for j, w in row if w >= MIN_SHARE])
        out["paragraphs"].append({"text": text, "words": [[s, e] for _, s, e in words], "arcs": arcs})
        for (w, _, _), a in zip(words, arcs):
            if a:
                print(f"{w:>12} -> " + ", ".join(f"{words[j][0]} {s:.2f}" for j, s in a))
    OUT.write_text(json.dumps(out, separators=(",", ":")) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
