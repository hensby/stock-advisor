'use client';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { useState } from 'react';

const SECTORS = ['Technology', 'Healthcare', 'Financial', 'Consumer Cyclical', 'Communication Services', 'Industrials', 'Consumer Defensive', 'Energy', 'Utilities', 'Real Estate', 'Basic Materials'];

export default function FilterSidebar({ filters, onChange }: { filters: Record<string, string | number>; onChange: (f: Record<string, string | number>) => void }) {
  const [local, setLocal] = useState(filters);

  const apply = () => onChange(local);
  const reset = () => { const r: Record<string, string | number> = {}; setLocal(r); onChange(r); };

  return (
    <aside className="w-56 shrink-0 space-y-4">
      <div className="bg-white shadow-card rounded-xl p-3">
        <h3 className="text-xs font-medium text-muted-foreground mb-2">行业</h3>
        <div className="space-y-1 max-h-40 overflow-y-auto">
          {SECTORS.map(s => (
            <label key={s} className="flex items-center gap-2 text-sm cursor-pointer hover:text-foreground">
              <input type="checkbox" checked={local.sector === s} onChange={() => setLocal(l => ({ ...l, sector: l.sector === s ? '' : s }))} className="rounded" />
              {s}
            </label>
          ))}
        </div>
      </div>

      <div className="bg-white shadow-card rounded-xl p-3">
        <h3 className="text-xs font-medium text-muted-foreground mb-2">最低综合评分</h3>
        <input type="range" min="0" max="100" value={String(local.min_composite || 0)}
          onChange={e => setLocal(l => ({ ...l, min_composite: Number(e.target.value) }))}
          className="w-full" />
        <span className="number-font text-sm">{local.min_composite || 0}</span>
      </div>

      <div className="flex gap-2">
        <Button size="sm" onClick={apply} className="flex-1">应用</Button>
        <Button size="sm" variant="outline" onClick={reset} className="flex-1">重置</Button>
      </div>
    </aside>
  );
}
