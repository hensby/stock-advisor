'use client';
import { useEffect, useRef } from 'react';
import type { ChartData } from '@/lib/types';

export default function PriceChartView({ ticker, data }: { ticker: string; data?: ChartData }) {
  const containerRef = useRef<HTMLDivElement>(null);

  // Simplified chart placeholder - in production, use createChart from lightweight-charts
  return (
    <div className="bg-white shadow-card rounded-xl overflow-hidden" style={{ height: 420 }}>
      <div className="flex items-center justify-between px-4 py-2 border-b border-slate-100">
        <span className="text-sm font-medium">{ticker} 走势图</span>
        <div className="flex gap-1">
          {['1M', '3M', '6M', '1Y'].map(r => (
            <button key={r} className="px-2 py-0.5 text-xs rounded shadow-card hover:bg-accent transition-colors">{r}</button>
          ))}
        </div>
      </div>
      <div ref={containerRef} className="p-4 flex items-center justify-center h-full">
        {data?.data?.length ? (
          <div className="w-full h-full">
            <div className="flex items-end gap-[2px] h-64 px-4">
              {data.data.slice(-100).map((c, i) => {
                const max = Math.max(...data.data.map(d => d.close || 0));
                const min = Math.min(...data.data.filter(d => d.close).map(d => d.close || 0));
                const range = max - min || 1;
                const h = ((c.close || min) - min) / range * 200 + 20;
                const up = (c.close || 0) >= (c.open || 0);
                return (
                  <div key={i} className="flex-1 flex flex-col justify-end items-center" title={`${c.date} O:${c.open} H:${c.high} L:${c.low} C:${c.close}`}>
                    <div style={{ height: `${(c.high || c.low || 0) - (c.low || c.low || 0)}` }} className="w-px bg-border/50" />
                    <div style={{ height: `${Math.max(1, Math.abs((c.close || 0) - (c.open || 0)))}` }}
                      className={`w-[80%] ${up ? 'bg-emerald-500/60' : 'bg-red-500/60'}`} />
                  </div>
                );
              })}
            </div>
            <p className="text-xs text-center text-muted-foreground mt-2">
              {data.data.length} 个交易日 · 最后收盘: ${data.data[data.data.length - 1]?.close?.toFixed(2)}
            </p>
          </div>
        ) : (
          <span className="text-sm text-muted-foreground">暂无价格数据</span>
        )}
      </div>
    </div>
  );
}
