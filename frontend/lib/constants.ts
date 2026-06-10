export const SIGNAL_COLORS: Record<string, string> = {
  strong_buy: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  buy: 'bg-green-50 text-green-700 border-green-200',
  hold: 'bg-slate-100 text-slate-600 border-slate-200',
  sell: 'bg-red-50 text-red-600 border-red-200',
  strong_sell: 'bg-rose-50 text-rose-700 border-rose-200',
};

export const SIGNAL_LABELS: Record<string, string> = {
  strong_buy: '强烈买入',
  buy: '买入',
  hold: '持有',
  sell: '卖出',
  strong_sell: '强烈卖出',
};

export const DEFAULT_WEIGHTS = {
  technical: 0.40,
  institutional: 0.30,
  youtube: 0.20,
  fundamental: 0.10,
};

export const CHART_RANGES = [
  { label: '1 月', value: '1m' },
  { label: '3 月', value: '3m' },
  { label: '6 月', value: '6m' },
  { label: '1 年', value: '1y' },
  { label: '全部', value: 'all' },
];
