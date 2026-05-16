import type { Bike, Price, BikeImage, BikeWithRelations, BikeListItem, BikeOption } from './types';

export async function getAllBikes(db: D1Database): Promise<BikeListItem[]> {
  const { results: bikes } = await db.prepare(
    'SELECT * FROM bikes ORDER BY brand, model, build'
  ).all<Bike>();

  const { results: prices } = await db.prepare(
    'SELECT * FROM prices'
  ).all<Price>();

  const { results: images } = await db.prepare(
    'SELECT * FROM images WHERE is_primary = 1'
  ).all<BikeImage>();

  const priceMap = new Map<number, Record<string, number>>();
  for (const p of prices) {
    if (!priceMap.has(p.bike_id)) priceMap.set(p.bike_id, {});
    priceMap.get(p.bike_id)![p.currency] = p.amount;
  }

  const imageMap = new Map<number, string>();
  for (const img of images) {
    imageMap.set(img.bike_id, img.url);
  }

  return bikes.map(b => ({
    id: b.id,
    slug: b.slug,
    brand: b.brand,
    model: b.model,
    build: b.build,
    country: b.country,
    status: b.status,
    motor: b.motor,
    peak_w: b.peak_w,
    peak_nm: b.peak_nm,
    battery_wh: b.battery_wh,
    removable: b.removable,
    front_travel_mm: b.front_travel_mm,
    rear_travel_mm: b.rear_travel_mm,
    frame: b.frame,
    weight_kg: b.weight_kg,
    primary_image: imageMap.get(b.id) ?? null,
    prices: priceMap.get(b.id) ?? {},
  }));
}

export async function getBikeBySlug(db: D1Database, slug: string): Promise<BikeWithRelations | null> {
  const bike = await db.prepare(
    'SELECT * FROM bikes WHERE slug = ?'
  ).bind(slug).first<Bike>();

  if (!bike) return null;

  const { results: prices } = await db.prepare(
    'SELECT * FROM prices WHERE bike_id = ? ORDER BY currency'
  ).bind(bike.id).all<Price>();

  const { results: images } = await db.prepare(
    'SELECT * FROM images WHERE bike_id = ? ORDER BY sort_order'
  ).bind(bike.id).all<BikeImage>();

  return { ...bike, prices, images };
}

export async function getAllBikeOptions(db: D1Database): Promise<BikeOption[]> {
  const { results } = await db.prepare(
    'SELECT slug, brand, model, build FROM bikes ORDER BY brand, model, build'
  ).all<BikeOption>();
  return results;
}

export async function getBikePairBySlugs(
  db: D1Database,
  slug1: string,
  slug2: string,
): Promise<[BikeWithRelations | null, BikeWithRelations | null]> {
  const [b1, b2] = await Promise.all([
    getBikeBySlug(db, slug1),
    getBikeBySlug(db, slug2),
  ]);
  return [b1, b2];
}
