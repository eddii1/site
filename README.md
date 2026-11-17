# eduardtudoran.com

Personal site and blog, built with [Astro](https://docs.astro.build).

## Commands

| Command           | What it does                                   |
| ----------------- | ---------------------------------------------- |
| `npm install`     | Install dependencies                           |
| `npm run dev`     | Dev server at `localhost:4321` (shows drafts)  |
| `npm run check`   | Type-check `.astro` and `.ts` files            |
| `npm run build`   | Build the site to `dist/` (drafts excluded)    |
| `npm run preview` | Serve the built site locally                   |

## Layout

| Path                        | What                                                   |
| --------------------------- | ------------------------------------------------------ |
| `src/pages/index.astro`     | Home page: bio, work and recent posts                  |
| `src/pages/writing/`        | Writing index and post pages                           |
| `src/content/writing/`      | Posts as Markdown/MDX. `draft: true` keeps one private |
| `src/layouts/Page.astro`    | Shared shell: head, header, main, footer               |
| `src/consts.ts`             | Site title, description, social links                  |
| `src/styles/global.css`     | Global styles and color tokens                         |

## Writing a post

Add `src/content/writing/<slug>.md` with this frontmatter:

```yaml
---
title: 'Post title'
description: 'One sentence for the post list, RSS and link previews.'
pubDate: '2026-11-05'
draft: true # remove to publish
---
```

## Deploy

GitHub Pages, through `.github/workflows/deploy.yml`: every push to `main` builds and deploys.

## Analytics

- Cloudflare Web Analytics: site-wide, script in `src/components/BaseHead.astro` (built pages only).
- GoatCounter (`eddii1`): counts post views and powers the view count at the end of each post
  (`src/components/ViewCount.astro`).
