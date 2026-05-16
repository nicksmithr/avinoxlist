import { useState, useMemo } from 'react';
import type { BikeListItem } from '../lib/types';

interface Props {
  bikes: BikeListItem[];
}

const CURRENCY_SYM: Record<string, string> = { gbp: '£', eur: '€', usd: '$', cad: 'C$', aud: 'A$' };
const EUR_RATES: Record<string, number> = { eur: 1, gbp: 0.845, usd: 1.08, cad: 1.50, aud: 1.68 };

function convert(amount: number, from: string, to: string): number {
  const inEur = amount / EUR_RATES[from];
  return Math.round(inEur * EUR_RATES[to]);
}

function pickPrice(prices: Record<string, number>, currency: string): { value: number; converted: boolean } | null {
  if (prices[currency]) return { value: prices[currency], converted: false };
  for (const src of ['gbp', 'eur', 'usd', 'cad', 'aud']) {
    if (prices[src]) return { value: convert(prices[src], src, currency), converted: true };
  }
  return null;
}

export default function BikeGrid({ bikes }: Props) {
  const [motor, setMotor] = useState('all');
  const [frame, setFrame] = useState('all');
  const [search, setSearch] = useState('');
  const [sort, setSort] = useState('weight-asc');
  const [currency, setCurrency] = useState('gbp');
  const [weightUnit, setWeightUnit] = useState<'kg' | 'lb'>('kg');

  const filtered = useMemo(() => {
    let result = bikes;
    if (motor !== 'all') result = result.filter(b => b.motor === motor);
    if (frame !== 'all') {
      result = result.filter(b => {
        const f = (b.frame || '').toLowerCase();
        return frame === 'carbon' ? f.includes('carbon') : (f.includes('alloy') || f.includes('alumin'));
      });
    }
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(b => `${b.brand} ${b.model} ${b.build}`.toLowerCase().includes(q));
    }
    const [field, dir] = sort.split('-');
    result = [...result].sort((a, b) => {
      let av: number, bv: number;
      if (field === 'price') {
        const pa = pickPrice(a.prices, currency);
        const pb = pickPrice(b.prices, currency);
        av = pa?.value ?? Infinity;
        bv = pb?.value ?? Infinity;
      } else if (field === 'weight') {
        av = a.weight_kg ?? Infinity;
        bv = b.weight_kg ?? Infinity;
      } else if (field === 'battery') {
        av = a.battery_wh ?? 0;
        bv = b.battery_wh ?? 0;
      } else {
        av = a.peak_w ?? 0;
        bv = b.peak_w ?? 0;
      }
      return dir === 'desc' ? bv - av : av - bv;
    });
    return result;
  }, [bikes, motor, frame, search, sort, currency]);

  const fmtWeight = (kg: number | null) => {
    if (!kg) return '—';
    return weightUnit === 'lb' ? `${(kg * 2.20462).toFixed(1)} lb` : `${kg.toFixed(1)} kg`;
  };

  return (
    <div>
      {/* Filter Bar */}
      <div class="sticky top-0 z-10 bg-[var(--color-bg)]/95 backdrop-blur-sm border-b border-[var(--color-border)] py-3 mb-8 flex flex-wrap items-center gap-2">
        <span class="text-[10px] font-semibold text-[var(--color-text-3)] uppercase tracking-wider">Motor</span>
        {['all', 'M2S', 'M2'].map(v => (
          <button
            key={v}
            onClick={() => setMotor(v)}
            class={`px-3 py-1 rounded-full text-xs font-medium transition-all ${motor === v ? 'bg-[var(--color-text)] text-white shadow-sm' : 'bg-[var(--color-surface)] text-[var(--color-text-2)] hover:bg-[var(--color-border)]'}`}
          >
            {v === 'all' ? 'All' : v}
          </button>
        ))}

        <div class="w-px h-5 bg-[var(--color-border)] mx-1" />

        <span class="text-[10px] font-semibold text-[var(--color-text-3)] uppercase tracking-wider">Frame</span>
        {['all', 'carbon', 'alloy'].map(v => (
          <button
            key={v}
            onClick={() => setFrame(v)}
            class={`px-3 py-1 rounded-full text-xs font-medium transition-all ${frame === v ? 'bg-[var(--color-text)] text-white shadow-sm' : 'bg-[var(--color-surface)] text-[var(--color-text-2)] hover:bg-[var(--color-border)]'}`}
          >
            {v === 'all' ? 'All' : v.charAt(0).toUpperCase() + v.slice(1)}
          </button>
        ))}

        <div class="w-px h-5 bg-[var(--color-border)] mx-1 hidden sm:block" />

        <div class="relative">
          <svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[var(--color-text-3)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="search"
            placeholder="Search…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            class="pl-8 pr-3 py-1.5 rounded-lg border border-[var(--color-border)] text-sm bg-transparent w-40 focus:outline-none focus:border-[var(--color-text-3)] focus:ring-1 focus:ring-[var(--color-text-3)]/20 transition-all placeholder:text-[var(--color-text-3)]"
          />
        </div>

        <div class="ml-auto flex items-center gap-1.5">
          <select value={sort} onChange={e => setSort(e.target.value)}
            class="px-2.5 py-1.5 rounded-lg border border-[var(--color-border)] text-xs bg-transparent text-[var(--color-text-2)] focus:outline-none">
            <option value="weight-asc">Weight ↑</option>
            <option value="weight-desc">Weight ↓</option>
            <option value="battery-desc">Battery ↓</option>
            <option value="price-asc">Price ↑</option>
            <option value="price-desc">Price ↓</option>
            <option value="peak-desc">Power ↓</option>
          </select>

          <select value={currency} onChange={e => setCurrency(e.target.value)}
            class="px-2.5 py-1.5 rounded-lg border border-[var(--color-border)] text-xs bg-transparent text-[var(--color-text-2)] focus:outline-none">
            <option value="gbp">£ GBP</option>
            <option value="eur">€ EUR</option>
            <option value="usd">$ USD</option>
            <option value="cad">C$ CAD</option>
            <option value="aud">A$ AUD</option>
          </select>

          <select value={weightUnit} onChange={e => setWeightUnit(e.target.value as 'kg' | 'lb')}
            class="px-2.5 py-1.5 rounded-lg border border-[var(--color-border)] text-xs bg-transparent text-[var(--color-text-2)] focus:outline-none">
            <option value="kg">kg</option>
            <option value="lb">lb</option>
          </select>
        </div>
      </div>

      <p class="text-xs text-[var(--color-text-3)] mb-5">
        Showing <strong class="text-[var(--color-text)] font-semibold">{filtered.length}</strong> of {bikes.length} builds
      </p>

      {/* Grid */}
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
        {filtered.map(bike => {
          const price = pickPrice(bike.prices, currency);
          return (
            <a
              key={bike.id}
              href={`/bikes/${bike.slug}`}
              class="group block bg-[var(--color-bg-card)] rounded-2xl border border-[var(--color-border)] overflow-hidden hover:border-[var(--color-text-3)] hover:shadow-lg hover:shadow-black/5 transition-all duration-200"
            >
              <div class="aspect-[4/3] bg-[var(--color-surface)] flex items-center justify-center overflow-hidden p-4">
                {bike.primary_image ? (
                  <img
                    src={bike.primary_image}
                    alt={`${bike.brand} ${bike.model}`}
                    class="bike-img max-w-full max-h-full object-contain group-hover:scale-[1.03] transition-transform duration-300"
                    loading="lazy"
                  />
                ) : (
                  <div class="text-5xl font-black text-[var(--color-border)]">{bike.brand[0]}</div>
                )}
              </div>
              <div class="p-4 pt-3">
                <p class="text-[10px] font-semibold text-[var(--color-text-3)] uppercase tracking-wider">{bike.brand}</p>
                <p class="font-bold text-[15px] leading-tight mt-0.5">{bike.model}</p>
                <p class="text-xs text-[var(--color-text-2)] mt-0.5 truncate">{bike.build}</p>
                <div class="mt-3 flex flex-wrap gap-x-3 gap-y-1 text-[11px] text-[var(--color-text-2)]">
                  <span class="inline-flex items-center gap-1">
                    <span class="inline-block w-1 h-1 rounded-full bg-[var(--color-accent)]" />
                    {bike.motor}
                  </span>
                  <span>{bike.battery_wh}Wh</span>
                  <span>{bike.front_travel_mm}/{bike.rear_travel_mm}mm</span>
                  {bike.weight_kg && <span>{fmtWeight(bike.weight_kg)}</span>}
                </div>
                <div class="mt-3 pt-3 border-t border-[var(--color-border)]">
                  {price ? (
                    <div class="flex items-baseline gap-1">
                      <span class="text-lg font-bold">
                        {price.converted && <span class="text-[var(--color-text-3)] font-normal">~</span>}
                        {CURRENCY_SYM[currency]}{price.value.toLocaleString()}
                      </span>
                      <span class="text-[10px] text-[var(--color-text-3)] uppercase">{currency}</span>
                    </div>
                  ) : (
                    <span class="text-xs text-[var(--color-text-3)]">Price TBA</span>
                  )}
                </div>
              </div>
            </a>
          );
        })}
      </div>
    </div>
  );
}
