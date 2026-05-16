import {
  catalog,
  aliases,
  type ComponentCategory,
  type ComponentPrices,
} from '../data/component-catalog';

export interface ComponentBreakdown {
  fork: number | null;
  shock: number | null;
  drivetrain: number | null;
  brakes: number | null;
  wheelset: number | null;
  dropper: number | null;
  total: number;
  matched: number;
  possible: number;
}

const CATEGORIES: ComponentCategory[] = [
  'fork', 'shock', 'drivetrain', 'brakes', 'wheelset', 'dropper',
];

function resolve(
  category: ComponentCategory,
  raw: string | null,
): ComponentPrices | null {
  if (!raw || raw === 'n/a' || raw === 'n/a (hardtail)') return null;

  const catPrices = catalog[category];
  const catAliases = aliases[category];

  // 1. Exact catalog key
  if (catPrices[raw]) return catPrices[raw];

  // 2. Alias
  const aliased = catAliases[raw];
  if (aliased === '_skip') return null;
  if (aliased && catPrices[aliased]) return catPrices[aliased];

  // 3. Longest prefix match against catalog keys (not aliases)
  let bestKey = '';
  for (const key of Object.keys(catPrices)) {
    if (key === '_default') continue;
    if (raw.startsWith(key) && key.length > bestKey.length) {
      bestKey = key;
    }
  }
  if (bestKey) return catPrices[bestKey];

  // 4. Longest prefix match against alias keys
  let bestAlias = '';
  for (const key of Object.keys(catAliases)) {
    if (raw.startsWith(key) && key.length > bestAlias.length) {
      bestAlias = key;
    }
  }
  if (bestAlias) {
    const target = catAliases[bestAlias];
    if (target === '_skip') return null;
    if (catPrices[target]) return catPrices[target];
  }

  // 5. Default
  return catPrices['_default'] ?? null;
}

export function getComponentValues(
  bike: {
    fork: string | null;
    shock: string | null;
    drivetrain: string | null;
    brakes: string | null;
    wheelset: string | null;
    dropper: string | null;
  },
  currency: 'gbp' | 'eur' | 'usd',
): ComponentBreakdown {
  let total = 0;
  let matched = 0;
  let possible = 0;

  const result: Record<string, number | null> = {};

  for (const cat of CATEGORIES) {
    const raw = bike[cat];
    if (!raw || raw === 'n/a' || raw === 'n/a (hardtail)') {
      result[cat] = null;
      continue;
    }
    possible++;
    const prices = resolve(cat, raw);
    if (prices) {
      result[cat] = prices[currency];
      total += prices[currency];
      matched++;
    } else {
      result[cat] = null;
    }
  }

  return {
    fork: result.fork ?? null,
    shock: result.shock ?? null,
    drivetrain: result.drivetrain ?? null,
    brakes: result.brakes ?? null,
    wheelset: result.wheelset ?? null,
    dropper: result.dropper ?? null,
    total,
    matched,
    possible,
  };
}

export interface ValidationResult {
  slug: string;
  brand: string;
  model: string;
  build: string;
  bikePrice: number | null;
  componentTotal: number;
  framePremium: number | null;
  matched: number;
  possible: number;
  status: 'ok' | 'over' | 'under' | 'no_price' | 'low_match';
}

export function validateBike(
  bike: {
    slug: string;
    brand: string;
    model: string;
    build: string;
    fork: string | null;
    shock: string | null;
    drivetrain: string | null;
    brakes: string | null;
    wheelset: string | null;
    dropper: string | null;
  },
  bikePrice: number | null,
  currency: 'gbp' | 'eur' | 'usd',
): ValidationResult {
  const cv = getComponentValues(bike, currency);

  if (!bikePrice) {
    return {
      slug: bike.slug,
      brand: bike.brand,
      model: bike.model,
      build: bike.build,
      bikePrice: null,
      componentTotal: cv.total,
      framePremium: null,
      matched: cv.matched,
      possible: cv.possible,
      status: 'no_price',
    };
  }

  const framePremium = bikePrice - cv.total;

  let status: ValidationResult['status'] = 'ok';
  if (cv.matched < cv.possible * 0.5) {
    status = 'low_match';
  } else if (framePremium < 1000) {
    status = 'over';
  } else if (framePremium > 8500) {
    status = 'under';
  }

  return {
    slug: bike.slug,
    brand: bike.brand,
    model: bike.model,
    build: bike.build,
    bikePrice,
    componentTotal: cv.total,
    framePremium,
    matched: cv.matched,
    possible: cv.possible,
    status,
  };
}
