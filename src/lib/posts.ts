import { getCollection } from 'astro:content';

/**
 * Posts, newest first. Drafts are included in dev and excluded from
 * production builds, so every page, the RSS feed and the sitemap agree.
 */
export async function getPosts() {
	const posts = await getCollection('writing', ({ data }) => import.meta.env.DEV || !data.draft);
	return posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}
