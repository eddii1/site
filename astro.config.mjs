// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig, fontProviders } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	site: 'https://eduardtudoran.com',
	integrations: [mdx(), sitemap()],
	markdown: {
		// Light theme so code blocks sit on the same pale panel as the rest of the page.
		shikiConfig: { theme: 'github-light' },
	},
	// Downloaded from Fontsource at build time and served from this site, so no third-party requests.
	fonts: [
		{
			provider: fontProviders.fontsource(),
			name: 'Source Serif 4',
			cssVariable: '--font-serif',
			weights: [400, 600, 700],
			styles: ['normal', 'italic'],
			subsets: ['latin', 'latin-ext'],
			fallbacks: ['Charter', 'Georgia', 'serif'],
		},
		{
			provider: fontProviders.fontsource(),
			name: 'Inter',
			cssVariable: '--font-sans',
			weights: [400, 500, 600, 700],
			styles: ['normal'],
			subsets: ['latin', 'latin-ext'],
			fallbacks: ['-apple-system', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
		},
	],
});
