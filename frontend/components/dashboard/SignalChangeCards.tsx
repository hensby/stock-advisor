'use client';
import Link from 'next/link';
import { ArrowUp, ArrowDown, ArrowRight } from 'lucide-react';
import { SIGNAL_LABELS, SIGNAL_COLORS } from '@/lib/constants';
import type { SignalChangeItem } from '@/lib/types';

export default function SignalChangeCards({ items }: { items: SignalChangeItem[] }) {
  if (!items.length) return (
    <div className="text-sm text-muted-foreground py-4">暂无信号变化</div>
  );

  return (
    <div>
      <h2 className="text-sm font-medium text-muted-foreground mb-3">📊 信号变化</h2>
      <div className="flex gap-3 overflow-x-auto pb-2">
        {items.map((item, i) => {
          const up = (item.composite_change ?? 0) >= 0;
          return (
            <Link key={i} href={`/stock/${item.ticker}`}
              className="shrink-0 w-48 bg-white shadow-card rounded-xl p-3 hover:border-primary/30 transition-colors"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-sm">{item.ticker}</span>
                {up ? <ArrowUp className="w-4 h-4 text-up" /> : <ArrowDown className="w-4 h-4 text-down" />}
              </div>
              <p className="text-xs text-muted-foreground">
                {SIGNAL_LABELS[item.previous_signal || ''] || item.previous_signal} → {SIGNAL_LABELS[item.current_signal || ''] || item.current_signal}
              </p>
              {item.composite_change != null && (
                <p className={`number-font text-xs mt-1 ${up ? 'text-up' : 'text-down'}`}>
                  {up ? '+' : ''}{item.composite_change.toFixed(0)} 分
                </p>
              )}
              {item.trigger_reasons.slice(0, 2).map((r, j) => (
                <p key={j} className="text-xs text-muted-foreground mt-0.5 truncate">{r}</p>
              ))}
            </Link>
          );
        })}
      </div>
    </div>
  );
}
