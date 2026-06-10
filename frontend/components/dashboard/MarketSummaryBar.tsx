'use client';
import { useQuery } from '@tanstack/react-query';
import { getMarketIndices } from '@/lib/api';
import type { MarketIndexValue } from '@/lib/types';

function IndexBadge({ label, data }: { label: string; data?: MarketIndexValue }) {
  if (!data?.value) return (
    <div className="bg-white shadow-card rounded-xl px-4 py-3">
      <span className="text-xs text-muted-foreground">{label}</span>
      <div className="text-sm text-muted-foreground mt-0.5">--</div>
    </div>
  );
  const up = (data.change_pct ?? 0) >= 0;
  return (
    <div className="bg-white shadow-card rounded-xl px-4 py-3">
      <span className="text-xs text-muted-foreground">{label}</span>
      <div className="flex items-center gap-2 mt-0.5">
        <span className="number-font text-sm font-medium">{data.value.toLocaleString()}</span>
        <span className={`number-font text-xs ${up ? 'text-up' : 'text-down'}`}>
          {up ? '+' : ''}{data.change_pct?.toFixed(2)}%
        </span>
      </div>
    </div>
  );
}

export default function MarketSummaryBar() {
  const { data } = useQuery({ queryKey: ['indices'], queryFn: getMarketIndices, refetchInterval: 60000 });
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      <IndexBadge label="S&P 500" data={data?.sp500} />
      <IndexBadge label="NASDAQ" data={data?.nasdaq} />
      <IndexBadge label="DOW JONES" data={data?.dow} />
      <IndexBadge label="VIX" data={data?.vix} />
    </div>
  );
}
