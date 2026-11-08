import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const writing = defineCollection({
	// Load Markdown and MDX files in the `src/content/writing/` directory.
	loader: glob({ base: './src/content/writing', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			// Shown under the title, in lists, and as the meta description.
			description: z.string(),
			// Transform string to Date object
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: z.optional(image()),
			// Published, but flagged as still changing.
			wip: z.boolean().default(false),
			// Drafts show up in `npm run dev` only, never in the built site.
			draft: z.boolean().default(false),
			// Extra entries for the meta row under the title, e.g. { Model: 'Llama 3 8B' }.
			meta: z.record(z.string(), z.string()).default({}),
		}),
});

export const collections = { writing };
