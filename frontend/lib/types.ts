export interface StockItem {
  ticker: string;
  name: string;
  sector?: string;
  market_cap?: number;
  composite_score?: number;
  signal?: string;
  price?: number;
  change?: number;
  change_pct?: number;
  volume?: number;
}

export interface ScoreBreakdown {
  technical_score?: number;
  institutional_score?: number;
  youtube_score?: number;
  fundamental_score?: number;
  composite_score?: number;
  signal?: string;
}

export interface TechnicalSignal {
  indicator: string;
  signal: string;
  value?: number;
  description: string;
}

export interface StockDetail extends StockItem {
  industry?: string;
  exchange?: string;
  previous_close?: number;
  scores?: ScoreBreakdown;
  technical_signals: TechnicalSignal[];
  investment_thesis?: string;
  bull_reasons: string[];
  bear_reasons: string[];
}

export interface ChartCandle {
  date: string;
  open?: number;
  high?: number;
  low?: number;
  close?: number;
  volume?: number;
  sma_20?: number;
  sma_50?: number;
  sma_200?: number;
  bb_upper?: number;
  bb_middle?: number;
  bb_lower?: number;
  macd?: number;
  macd_signal?: number;
  rsi?: number;
}

export interface ChartData {
  ticker: string;
  data: ChartCandle[];
}

export interface SignalEvent {
  date: string;
  signal?: string;
  composite_score?: number;
  trigger_reasons: string[];
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface Briefing {
  date: string;
  market_summary?: MarketSummary;
  signal_changes: SignalChangeItem[];
  top_picks: StockItem[];
  sector_sentiment: SectorSentiment[];
  risk_reminders: string[];
}

export interface MarketIndexValue {
  value?: number;
  change?: number;
  change_pct?: number;
}

export interface MarketSummary {
  sp500?: MarketIndexValue;
  nasdaq?: MarketIndexValue;
  dow?: MarketIndexValue;
  vix?: MarketIndexValue;
}

export interface SignalChangeItem {
  ticker: string;
  name?: string;
  previous_signal?: string;
  current_signal?: string;
  composite_change?: number;
  trigger_reasons: string[];
}

export interface SectorSentiment {
  sector: string;
  institutional_avg_score?: number;
  youtube_avg_score?: number;
}

export interface Watchlist {
  id: number;
  name: string;
  item_count: number;
  stocks: StockItem[];
}

export interface ScoringWeights {
  technical: number;
  institutional: number;
  youtube: number;
  fundamental: number;
}
