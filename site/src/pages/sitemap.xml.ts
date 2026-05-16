import type { APIRoute } from 'astro';
import { getAllBikeOptions } from '../lib/db';
import { env } from 'cloudflare:workers';

export const GET: APIRoute = async () => {
  const bikes = await getAllBikeOptions(env.DB);
  const base = 'https://avinoxlist.com';

  const urls: string[] = [];

  // Homepage
  urls.push(base + '/');

  // Individual bike pages
  for (const b of bikes) {
    urls.push(`${base}/bikes/${b.slug}`);
  }

  // Compare landing
  urls.push(`${base}/compare/`);

  // Same-brand comparisons (all pairs within each brand)
  const byBrand: Record<string, typeof bikes> = {};
  for (const b of bikes) {
    (byBrand[b.brand] ??= []).push(b);
  }
  for (const brandBikes of Object.values(byBrand)) {
    for (let i = 0; i < brandBikes.length; i++) {
      for (let j = i + 1; j < brandBikes.length; j++) {
        const [a, b] = brandBikes[i].slug < brandBikes[j].slug
          ? [brandBikes[i].slug, brandBikes[j].slug]
          : [brandBikes[j].slug, brandBikes[i].slug];
        urls.push(`${base}/compare/${a}-vs-${b}`);
      }
    }
  }

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url><loc>${u}</loc></url>`).join('\n')}
</urlset>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml' },
  });
};
