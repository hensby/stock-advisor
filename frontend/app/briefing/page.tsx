'use client';
import { useQuery } from '@tanstack/react-query';
import { getBriefing } from '@/lib/api';
import { SIGNAL_LABELS, SIGNAL_COLORS } from '@/lib/constants';
import { ArrowUp, ArrowDown } from 'lucide-react';
import Link from 'next/link';

export default function BriefingPage() {
  const { data, isLoading } = useQuery({ queryKey: ['briefing'], queryFn: () => getBriefing() });

  if (isLoading) return <div className="p-6 text-muted-foreground">加载中...</div>;
  if (!data) return <div className="p-6 text-muted-foreground">暂无简报数据</div>;

  return (
    <div className="p-6 space-y-6 max-w-[1440px] mx-auto">
      <div>
        <h1 className="text-lg font-bold">每日简报</h1>
        <p className="text-sm text-muted-foreground">{data.date}</p>
      </div>

      {/* Signal Changes */}
      <div className="bg-white shadow-card rounded-xl p-4">
        <h2 className="text-sm font-medium mb-3">📊 信号变化</h2>
        {data.signal_changes.length ? (
          <div className="space-y-2">
            {data.signal_changes.map((item, i) => {
              const up = (item.composite_change ?? 0) >= 0;
              return (
                <div key={i} className="flex items-center gap-4 py-2 border-b border-slate-100/50 last:border-0">
                  <Link href={`/stock/${item.ticker}`} className="font-medium text-sm hover:text-primary w-16">{item.ticker}</Link>
                  <span className="text-xs text-muted-foreground">{SIGNAL_LABELS[item.previous_signal || '']} → {SIGNAL_LABELS[item.current_signal || '']}</span>
                  {item.composite_change != null && (
                    <span className={`number-font text-xs flex items-center gap-0.5 ${up ? 'text-up' : 'text-down'}`}>
                      {up ? <ArrowUp className="w-3 h-3" /> : <ArrowDown className="w-3 h-3" />}
                      {up ? '+' : ''}{item.composite_change.toFixed(0)}
                    </span>
                  )}
                  <span className="text-xs text-muted-foreground flex-1">{item.trigger_reasons.join(' · ')}</span>
                </div>
              );
            })}
          </div>
        ) : <p className="text-sm text-muted-foreground">今日无信号变化</p>}
      </div>

      {/* Top 10 */}
      <div className="bg-white shadow-card rounded-xl overflow-hidden">
        <div className="px-4 py-3 border-b border-slate-100">
          <h2 className="text-sm font-medium">🔥 今日优选 Top 10</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-100 text-xs text-muted-foreground">
                <th className="text-left px-4 py-2 font-medium">#</th>
                <th className="text-left px-4 py-2 font-medium">股票</th>
                <th className="text-right px-4 py-2 font-medium">综合评分</th>
                <th className="text-right px-4 py-2 font-medium">信号</th>
              </tr>
            </thead>
            <tbody>
              {data.top_picks.map((item, i) => (
                <tr key={item.ticker} className="border-b border-slate-100/50 hover:bg-accent/50">
                  <td className="px-4 py-2.5 text-muted-foreground">{i + 1}</td>
                  <td className="px-4 py-2.5">
                    <Link href={`/stock/${item.ticker}`} className="font-medium hover:text-primary">{item.ticker}</Link>
                    <span className="text-muted-foreground ml-1.5">{item.name?.slice(0, 20)}</span>
                  </td>
                  <td className="px-4 py-2.5 text-right number-font">{item.composite_score?.toFixed(0)}</td>
                  <td className="px-4 py-2.5 text-right">
                    <span className={`px-2 py-0.5 rounded text-xs border ${SIGNAL_COLORS[item.signal || '']}`}>
                      {SIGNAL_LABELS[item.signal || ''] || item.signal}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {data.risk_reminders.length > 0 && (
        <div className="border border-destructive/20 bg-destructive/5 rounded-lg p-4">
          {data.risk_reminders.map((r, i) => <p key={i} className="text-destructive text-sm">{r}</p>)}
        </div>
      )}
    </div>
  );
}
