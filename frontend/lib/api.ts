const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    if (res.status === 404) throw new Error('Not found');
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

import type { StockItem, StockDetail, ChartData, SignalEvent, PaginatedResponse, Briefing, Watchlist, ScoringWeights } from './types';

export async function getStocks(params: Record<string, string | number> = {}): Promise<PaginatedResponse<StockItem>> {
  const qs = new URLSearchParams(Object.entries(params).map(([k, v]) => [k, String(v)])).toString();
  return fetchAPI(`/stocks?${qs}`);
}

export async function getStockDetail(ticker: string): Promise<StockDetail> {
  return fetchAPI(`/stocks/${ticker}`);
}

export async function getStockChart(ticker: string, range = '1y'): Promise<ChartData> {
  return fetchAPI(`/stocks/${ticker}/chart?range=${range}`);
}

export async function getStockSignals(ticker: string): Promise<{ history: SignalEvent[] }> {
  return fetchAPI(`/stocks/${ticker}/signals`);
}

export async function getScreener(params: Record<string, string | number> = {}): Promise<PaginatedResponse<StockItem>> {
  const qs = new URLSearchParams(Object.entries(params).map(([k, v]) => [k, String(v)])).toString();
  return fetchAPI(`/screener?${qs}`);
}

export async function getBriefing(date?: string): Promise<Briefing> {
  return fetchAPI(date ? `/briefing?date=${date}` : '/briefing');
}

export async function getWatchlists(): Promise<Watchlist[]> {
  return fetchAPI('/watchlist');
}

export async function createWatchlist(name: string): Promise<Watchlist> {
  return fetchAPI('/watchlist', { method: 'POST', body: JSON.stringify({ name }) });
}

export async function deleteWatchlist(id: number): Promise<void> {
  await fetch(`${API_BASE}/watchlist/${id}`, { method: 'DELETE' });
}

export async function addToWatchlist(watchlistId: number, ticker: string): Promise<void> {
  await fetch(`${API_BASE}/watchlist/${watchlistId}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ticker }),
  });
}

export async function removeFromWatchlist(watchlistId: number, ticker: string): Promise<void> {
  await fetch(`${API_BASE}/watchlist/${watchlistId}/items/${ticker}`, { method: 'DELETE' });
}

export async function getScoringWeights(): Promise<ScoringWeights> {
  return fetchAPI('/settings/scoring-weights');
}

export async function updateScoringWeights(weights: ScoringWeights): Promise<ScoringWeights> {
  return fetchAPI('/settings/scoring-weights', { method: 'PUT', body: JSON.stringify(weights) });
}

export async function getMarketIndices(): Promise<{
  sp500: { value: number; change: number; change_pct: number };
  nasdaq: { value: number; change: number; change_pct: number };
  dow: { value: number; change: number; change_pct: number };
  vix: { value: number; change: number; change_pct: number };
}> {
  return fetchAPI('/market/indices');
}
