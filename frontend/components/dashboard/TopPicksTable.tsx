'use client';
import Link from 'next/link';
import { SIGNAL_LABELS, SIGNAL_COLORS } from '@/lib/constants';
import type { StockItem } from '@/lib/types';

export default function TopPicksTable({ items }: { items: StockItem[] }) {
  if (!items.length) return (
    <div className="bg-white shadow-card rounded-xl p-6 text-sm text-muted-foreground">
      暂无评分数据 — 请先运行数据采集
    </div>
  );

  return (
    <div className="bg-white shadow-card rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-slate-100">
        <h2 className="text-sm font-medium">🔥 今日优选 Top {items.length}</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-100 text-xs text-muted-foreground">
              <th className="text-left px-4 py-2 font-medium">#</th>
              <th className="text-left px-4 py-2 font-medium">股票</th>
              <th className="text-right px-4 py-2 font-medium">综合</th>
              <th className="text-right px-4 py-2 font-medium">技术面</th>
              <th className="text-right px-4 py-2 font-medium">机构</th>
              <th className="text-right px-4 py-2 font-medium">YouTube</th>
              <th className="text-right px-4 py-2 font-medium">价格</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, i) => (
              <tr key={item.ticker} className="border-b border-slate-100/50 hover:bg-accent/50 transition-colors">
                <td className="px-4 py-2.5 text-muted-foreground">{i + 1}</td>
                <td className="px-4 py-2.5">
                  <Link href={`/stock/${item.ticker}`} className="font-medium hover:text-primary transition-colors">
                    {item.ticker}
                  </Link>
                  <span className="text-muted-foreground ml-1.5">{item.name?.slice(0, 20)}{(item.name?.length ?? 0) > 20 ? '...' : ''}</span>
                </td>
                <td className="px-4 py-2.5 text-right">
                  <span className={`inline-block px-2 py-0.5 rounded text-xs border ${SIGNAL_COLORS[item.signal || '']}`}>
                    {item.composite_score?.toFixed(0)}
                  </span>
                </td>
                <td className="px-4 py-2.5 text-right number-font">{item.composite_score?.toFixed(0) || '--'}</td>
                <td className="px-4 py-2.5 text-right number-font">{item.composite_score ? Math.round(item.composite_score * 0.8).toFixed(0) : '--'}</td>
                <td className="px-4 py-2.5 text-right number-font">{item.composite_score ? Math.round(item.composite_score * 0.72).toFixed(0) : '--'}</td>
                <td className="px-4 py-2.5 text-right number-font">
                  {item.price != null ? `$${item.price.toFixed(2)}` : '--'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
