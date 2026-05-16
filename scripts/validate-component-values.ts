import * as fs from 'fs';
import * as path from 'path';
import { validateBike, getComponentValues } from '../site/src/lib/component-value';

const indexPath = path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(indexPath, 'utf-8');
const match = html.match(/const BIKES = (.*?);\s*const STATS =/s);
if (!match) throw new Error('Could not find BIKES JSON');
const bikes: any[] = JSON.parse(match[1]);

const currency = 'gbp' as const;
console.log(`\nValidating ${bikes.length} bikes against component catalog (${currency.toUpperCase()})\n`);

function slugify(brand: string, model: string, build: string): string {
  const modelWords = new Set(model.toLowerCase().split(' '));
  const buildNorm = build.toLowerCase().replace(/[^a-z0-9 ]+/g, ' ');
  const buildWords = new Set(buildNorm.split(' ').filter(Boolean));
  const modelSubset = [...modelWords].every(w => buildWords.has(w));
  const text = modelSubset ? `${brand} ${build}` : `${brand} ${model} ${build}`;
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

const results = bikes.map(b => {
  const slug = slugify(b.brand, b.model, b.build);
  return validateBike(
    { slug, brand: b.brand, model: b.model, build: b.build,
      fork: b.fork, shock: b.shock, drivetrain: b.drivetrain,
      brakes: b.brakes, wheelset: b.wheelset, dropper: b.dropper },
    b[currency],
    currency,
  );
});

// Summary
const ok = results.filter(r => r.status === 'ok');
const over = results.filter(r => r.status === 'over');
const under = results.filter(r => r.status === 'under');
const noPrice = results.filter(r => r.status === 'no_price');
const lowMatch = results.filter(r => r.status === 'low_match');

console.log(`✓ OK:        ${ok.length}`);
console.log(`⚠ Over:      ${over.length}  (components > bike price - £1500)`);
console.log(`⚠ Under:     ${under.length}  (components < bike price - £6000)`);
console.log(`○ No price:  ${noPrice.length}`);
console.log(`○ Low match: ${lowMatch.length}  (<50% components matched)\n`);

// Detail table
const pad = (s: string, n: number) => s.slice(0, n).padEnd(n);
const rpad = (s: string, n: number) => s.slice(0, n).padStart(n);

console.log(
  pad('Brand/Model/Build', 55) +
  rpad('Price', 8) +
  rpad('CV', 8) +
  rpad('Premium', 9) +
  rpad('M/P', 5) +
  '  Status'
);
console.log('-'.repeat(90));

for (const r of results) {
  const label = `${r.brand} ${r.model} ${r.build}`;
  const price = r.bikePrice ? `£${r.bikePrice}` : '-';
  const cv = `£${r.componentTotal}`;
  const prem = r.framePremium !== null ? `£${r.framePremium}` : '-';
  const match = `${r.matched}/${r.possible}`;
  const status = r.status === 'ok' ? '✓' :
                 r.status === 'over' ? '⚠ OVER' :
                 r.status === 'under' ? '⚠ UNDER' :
                 r.status === 'no_price' ? '○' :
                 '⚠ LOW';
  console.log(
    pad(label, 55) +
    rpad(price, 8) +
    rpad(cv, 8) +
    rpad(prem, 9) +
    rpad(match, 5) +
    `  ${status}`
  );
}

// Show unmatched components
console.log('\n\n=== UNMATCHED COMPONENTS ===\n');
const unmatched: Record<string, Set<string>> = { fork: new Set(), shock: new Set(), drivetrain: new Set(), brakes: new Set(), wheelset: new Set(), dropper: new Set() };

for (const b of bikes) {
  for (const cat of ['fork', 'shock', 'drivetrain', 'brakes', 'wheelset', 'dropper'] as const) {
    const raw = b[cat];
    if (!raw || raw === 'n/a' || raw === 'n/a (hardtail)') continue;
    const cv = getComponentValues({ fork: null, shock: null, drivetrain: null, brakes: null, wheelset: null, dropper: null, [cat]: raw }, currency);
    if (cv[cat] === null) {
      unmatched[cat].add(raw);
    }
  }
}

for (const [cat, values] of Object.entries(unmatched)) {
  if (values.size > 0) {
    console.log(`${cat}: ${values.size} unmatched`);
    for (const v of values) console.log(`  - ${v}`);
  }
}
