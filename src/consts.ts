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

export interface Project {
	title: string;
	href: string;
	/** One line, shown after the title. */
	description: string;
	/** Optional small print under the item, e.g. data sources or credits. */
	note?: string;
}

/**
 * Home page lists. A section only shows once it has at least one entry. Example:
 * { title: 'Drone search', href: '/writing/drone-search-grok-hackathon/', description: 'a toy drone that finds objects on its own' }
 */
export const WORK: Project[] = [];
export const SIDE_PROJECTS: Project[] = [];
