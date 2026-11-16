// Site-wide data. Import from anywhere with `import { ... } from '../consts'`.

export const SITE_TITLE = 'Eduard Tudoran';
export const SITE_DESCRIPTION =
	'Eduard Tudoran - applied AI engineer in Milan. Agents, evaluation, and write-ups of things I build.';

/** The row of links under your name on the home page. */
export const SOCIAL_LINKS: Link[] = [
	{ label: 'LinkedIn', href: 'https://www.linkedin.com/in/eduard-tudoran/' },
	{ label: 'GitHub', href: 'https://github.com/eddii1' },
	{ label: 'Twitter', href: 'https://x.com/tudoranedi' },
	{ label: 'Email', href: 'mailto:tudoranedi@gmail.com' },
];

export interface Link {
	label: string;
	href: string;
}

/** One line under the bio: what you are working on right now. Empty hides it. */
export const NOW = 'measuring whether a LoRA backdoor in a small open model survives normal evals, and what catches it.';

export interface Project {
	title: string;
	href: string;
	/** One line with the result, shown under the title. */
	description: string;
	/** Short context on the right, e.g. the year or the event. */
	meta: string;
}

/**
 * Empty hides the section. Drafted entries, to put back later:
 * { title: 'Teaching a toy drone to scan rooms on its own', href: '/writing/seek/', meta: 'Grok Hackathon, 2026',
 *   description: 'Grok flies a €279 drone from one sentence; a depth map keeps it safe. 5 confirmed finds in real flights.' }
 * { title: 'Grading its own exam', href: 'https://github.com/eddii1/epistemics-sprint', meta: 'Apart Research, 2026',
 *   description: "One line in a chatbot's reply erases DarkBench's flags on six LLM graders; a second question to the grader restores them." }
 */
export const PROJECTS: Project[] = [];

export interface Role {
	org: string;
	role: string;
	dates: string;
	/** What you did there, one line. */
	description: string;
	href?: string;
}

export const WORK: Role[] = [
	{
		org: 'AINEXXO',
		role: 'AI engineer, Milan',
		dates: '2026 - now',
		description: 'Document extraction and evaluation for RAG and agent systems.',
	},
	{
		org: 'FOREO',
		role: 'AI engineer intern',
		dates: '2026',
		description: 'Multimodal defect extraction with LangGraph, with cost-aware model routing.',
	},
	{
		org: 'MidFlow AI',
		role: 'Founding AI engineer, Bucharest',
		dates: '2025 - 2026',
		description: 'Built the product from zero: document extraction, an LLM eval harness and the platform around them.',
	},
];
