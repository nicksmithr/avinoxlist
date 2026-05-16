import { useState } from 'react';
import type { BikeOption } from '../lib/types';

interface Props {
  allBikes: BikeOption[];
  initialSlug1: string;
  initialSlug2: string;
}

export default function BikeCompare({ allBikes, initialSlug1, initialSlug2 }: Props) {
  const [slug1, setSlug1] = useState(initialSlug1);
  const [slug2, setSlug2] = useState(initialSlug2);

  function navigate() {
    const s1 = slug1;
    const s2 = slug2;
    if (!s1 || !s2 || s1 === s2) return;
    const [a, b] = s1 < s2 ? [s1, s2] : [s2, s1];
    window.location.href = `/compare/${a}-vs-${b}`;
  }

  function handleChange(side: 1 | 2, value: string) {
    if (side === 1) setSlug1(value);
    else setSlug2(value);
  }

  const canCompare = slug1 && slug2 && slug1 !== slug2;

  const grouped = allBikes.reduce<Record<string, BikeOption[]>>((acc, b) => {
    (acc[b.brand] ??= []).push(b);
    return acc;
  }, {});

  return (
    <div className="mt-6 flex flex-col sm:flex-row items-stretch sm:items-end gap-3">
      <div className="flex-1">
        <label className="block text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-3)] font-medium mb-1.5">
          Bike 1
        </label>
        <select
          value={slug1}
          onChange={e => handleChange(1, e.target.value)}
          className="w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] appearance-none"
        >
          <option value="">Select a bike...</option>
          {Object.entries(grouped).map(([brand, bikes]) => (
            <optgroup key={brand} label={brand}>
              {bikes.map(b => (
                <option key={b.slug} value={b.slug}>
                  {b.model} — {b.build}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
      </div>

      <div className="flex items-center justify-center text-[var(--color-text-3)] font-bold text-lg px-2 py-2">
        vs
      </div>

      <div className="flex-1">
        <label className="block text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-3)] font-medium mb-1.5">
          Bike 2
        </label>
        <select
          value={slug2}
          onChange={e => handleChange(2, e.target.value)}
          className="w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] appearance-none"
        >
          <option value="">Select a bike...</option>
          {Object.entries(grouped).map(([brand, bikes]) => (
            <optgroup key={brand} label={brand}>
              {bikes.map(b => (
                <option key={b.slug} value={b.slug}>
                  {b.model} — {b.build}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
      </div>

      <button
        onClick={navigate}
        disabled={!canCompare}
        className="px-6 py-2.5 rounded-xl bg-[var(--color-text)] text-white text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-30 disabled:cursor-not-allowed whitespace-nowrap"
      >
        Compare
      </button>
    </div>
  );
}
