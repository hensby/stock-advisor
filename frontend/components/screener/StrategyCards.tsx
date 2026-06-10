'use client';
import { TrendingUp, RefreshCw, Search, Zap, Landmark, Video, LucideIcon } from 'lucide-react';

interface Strategy {
  id: string;
  name: string;
  desc: string;
  icon: LucideIcon;
  params: Record<string, number>;
}

const STRATEGIES: Strategy[] = [
  { id: 'technical_breakout', name: '技术面突破', desc: '金叉+量增+机构上调', icon: TrendingUp, params: { min_technical_score: 70, min_institutional_score: 60 } },
  { id: 'reversal_capture', name: '趋势反转捕捉', desc: 'RSI超卖+机构逆势看好', icon: RefreshCw, params: { min_institutional_score: 60 } },
  { id: 'value_discovery', name: '价值发现', desc: '低PE+回购增加', icon: Search, params: {} },
  { id: 'momentum_continuation', name: '动量延续', desc: 'ADX>25趋势强+RSI不极端', icon: Zap, params: { min_technical_score: 60 } },
  { id: 'smart_money', name: '跟随聪明钱', desc: '内部人大举买入+13F增持', icon: Landmark, params: { min_institutional_score: 70 } },
  { id: 'youtube_heat', name: 'YouTube热度', desc: 'YT一致看多+播放量激增', icon: Video, params: { min_youtube_score: 70 } },
];

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default function StrategyCards({ onSelect }: { onSelect: (params: any) => void }) {
  return (
    <div>
      <h2 className="text-sm font-medium text-muted-foreground mb-3">🎯 选股策略</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {STRATEGIES.map(s => {
          const Icon = s.icon;
          return (
            <button key={s.id} onClick={() => onSelect(s.params)}
              className="bg-white shadow-card rounded-xl p-3 text-left hover:border-primary/30 transition-colors"
            >
              <Icon className="w-5 h-5 text-primary mb-2" />
              <div className="text-sm font-medium">{s.name}</div>
              <div className="text-xs text-muted-foreground mt-0.5">{s.desc}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
