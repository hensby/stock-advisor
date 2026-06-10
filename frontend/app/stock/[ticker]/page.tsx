'use client';
import { useQuery } from '@tanstack/react-query';
import { useParams } from 'next/navigation';
import { getStockDetail, getStockChart, getStockSignals } from '@/lib/api';
import { PageSkeleton } from '@/components/ui/loading-skeleton';
import StockHeader from '@/components/stock-detail/StockHeader';
import AddToWatchlist from '@/components/stock-detail/AddToWatchlist';
import PriceChartView from '@/components/stock-detail/PriceChartView';
import ScoreBreakdownView from '@/components/stock-detail/ScoreBreakdownView';
import InvestmentThesisView from '@/components/stock-detail/InvestmentThesisView';
import SignalTimeline from '@/components/stock-detail/SignalTimeline';

export default function StockDetailPage() {
  const params = useParams();
  const ticker = (params.ticker as string).toUpperCase();

  const { data: stock, isLoading, error } = useQuery({
    queryKey: ['stock', ticker],
    queryFn: () => getStockDetail(ticker),
    enabled: !!ticker,
    retry: 1,
  });

  const { data: chartData } = useQuery({
    queryKey: ['chart', ticker],
    queryFn: () => getStockChart(ticker),
    enabled: !!ticker,
  });

  const { data: signalData } = useQuery({
    queryKey: ['signals', ticker],
    queryFn: () => getStockSignals(ticker),
    enabled: !!ticker,
  });

  if (isLoading) return <PageSkeleton />;
  if (error || !stock) return (
    <div className="p-6 text-center text-slate-500">
      股票 {ticker} 未找到或数据加载失败
    </div>
  );

  return (
    <div className="p-6 space-y-6 max-w-[1440px] mx-auto">
      <div className="flex items-start justify-between">
        <div className="flex-1"><StockHeader stock={stock} /></div>
        <AddToWatchlist ticker={ticker} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <PriceChartView ticker={ticker} data={chartData} />
        </div>
        <div className="space-y-4">
          <ScoreBreakdownView scores={stock.scores} />
          <div className="bg-white rounded-xl p-4">
            <h3 className="text-sm font-medium mb-3">技术信号</h3>
            <div className="space-y-2">
              {stock.technical_signals?.length ? stock.technical_signals.map((sig, i) => (
                <div key={i} className="flex items-center justify-between py-1.5 border-b border-slate-100 last:border-0">
                  <span className="text-sm text-slate-700">{sig.indicator}</span>
                  <span className={`text-xs px-2 py-0.5 rounded border ${
                    sig.signal === 'bullish' ? 'bg-emerald-50 border-emerald-200 text-emerald-700' :
                    sig.signal === 'bearish' ? 'bg-red-50 border-red-200 text-red-700' :
                    'bg-slate-100 border-slate-200 text-slate-600'
                  }`}>{sig.description}</span>
                </div>
              )) : <p className="text-xs text-slate-400">暂无技术信号数据</p>}
            </div>
          </div>
        </div>
      </div>

      <InvestmentThesisView thesis={stock.investment_thesis} bullReasons={stock.bull_reasons} bearReasons={stock.bear_reasons} />
      <SignalTimeline history={signalData?.history || []} />
    </div>
  );
}
