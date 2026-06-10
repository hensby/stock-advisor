'use client';
import Link from 'next/link';
import { SIGNAL_LABELS, SIGNAL_COLORS } from '@/lib/constants';
import type { StockItem, PaginatedResponse } from '@/lib/types';

export default function ResultsTable({ data }: { data?: PaginatedResponse<StockItem> }) {
  const items = data?.items || [];

  if (!items.length) return (
    <div className="bg-white shadow-card rounded-xl p-6 text-sm text-muted-foreground text-center">
      没有匹配的股票 — 请先运行数据采集或调整筛选条件
    </div>
  );

  return (
    <div className="bg-white shadow-card rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
        <h2 className="text-sm font-medium">结果 ({data?.total || 0})</h2>
        <span className="text-xs text-muted-foreground">第 {data?.page || 1} 页</span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-100 text-xs text-muted-foreground">
              <th className="text-left px-4 py-2 font-medium">代码</th>
              <th className="text-left px-4 py-2 font-medium">名称</th>
              <th className="text-left px-4 py-2 font-medium">行业</th>
              <th className="text-right px-4 py-2 font-medium">综合评分</th>
              <th className="text-right px-4 py-2 font-medium">信号</th>
              <th className="text-right px-4 py-2 font-medium">价格</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.ticker} className="border-b border-slate-100/50 hover:bg-accent/50 transition-colors">
                <td className="px-4 py-2.5">
                  <Link href={`/stock/${item.ticker}`} className="font-medium hover:text-primary transition-colors">{item.ticker}</Link>
                </td>
                <td className="px-4 py-2.5 text-muted-foreground">{item.name?.slice(0, 25)}</td>
                <td className="px-4 py-2.5 text-muted-foreground">{item.sector || '--'}</td>
                <td className="px-4 py-2.5 text-right number-font">{item.composite_score?.toFixed(0) || '--'}</td>
                <td className="px-4 py-2.5 text-right">
                  <span className={`inline-block px-2 py-0.5 rounded text-xs border ${SIGNAL_COLORS[item.signal || '']}`}>
                    {SIGNAL_LABELS[item.signal || ''] || item.signal}
                  </span>
                </td>
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
