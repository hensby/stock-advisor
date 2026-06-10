'use client';
import { useQuery } from '@tanstack/react-query';
import { getBriefing } from '@/lib/api';
import { PageSkeleton } from '@/components/ui/loading-skeleton';
import MarketSummaryBar from '@/components/dashboard/MarketSummaryBar';
import SignalChangeCards from '@/components/dashboard/SignalChangeCards';
import TopPicksTable from '@/components/dashboard/TopPicksTable';
import SentimentPulseChart from '@/components/dashboard/SentimentPulseChart';

export default function DashboardPage() {
  const { data: briefing, isLoading, error } = useQuery({
    queryKey: ['briefing'],
    queryFn: () => getBriefing(),
    retry: 1,
  });

  if (isLoading) return <PageSkeleton />;

  if (error) return (
    <div className="p-6 text-center">
      <p className="text-slate-500 mb-2">数据加载失败</p>
      <p className="text-sm text-slate-400">请确认后端已启动并已运行 <code className="bg-slate-100 px-1 rounded">python scripts/seed_all.py</code></p>
    </div>
  );

  return (
    <div className="p-6 space-y-6 max-w-[1440px] mx-auto">
      <MarketSummaryBar />
      <SignalChangeCards items={briefing?.signal_changes || []} />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <TopPicksTable items={briefing?.top_picks || []} />
        </div>
        <SentimentPulseChart sectors={briefing?.sector_sentiment || []} />
      </div>
      {briefing?.risk_reminders?.length ? (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
          {briefing.risk_reminders.map((r, i) => (
            <p key={i} className="text-amber-700 text-sm">{r}</p>
          ))}
        </div>
      ) : null}
    </div>
  );
}
