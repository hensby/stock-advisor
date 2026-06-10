import { SIGNAL_LABELS, SIGNAL_COLORS } from '@/lib/constants';
import type { StockDetail } from '@/lib/types';

export default function StockHeader({ stock }: { stock: StockDetail }) {
  const up = (stock.change_pct ?? 0) >= 0;
  return (
    <div className="bg-white shadow-card rounded-xl p-4 flex flex-wrap items-center gap-6">
      <div>
        <h1 className="text-xl font-bold">{stock.ticker}</h1>
        <p className="text-sm text-muted-foreground">{stock.name}</p>
      </div>
      <div className="flex items-baseline gap-3">
        <span className="number-font text-2xl font-semibold">${stock.price?.toFixed(2) || '--'}</span>
        {stock.change != null && (
          <span className={`number-font text-sm ${up ? 'text-up' : 'text-down'}`}>
            {up ? '+' : ''}{stock.change?.toFixed(2)} ({up ? '+' : ''}{stock.change_pct?.toFixed(2)}%)
          </span>
        )}
      </div>
      <div className="flex-1" />
      {stock.signal && (
        <span className={`px-3 py-1.5 rounded-md text-sm font-medium border ${SIGNAL_COLORS[stock.signal]}`}>
          {SIGNAL_LABELS[stock.signal]} {stock.composite_score?.toFixed(0)}分
        </span>
      )}
      <div className="text-xs text-muted-foreground">
        {stock.sector} · {stock.industry}
      </div>
    </div>
  );
}
