'use client';
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getScreener } from '@/lib/api';
import { TableSkeleton } from '@/components/ui/loading-skeleton';
import StrategyCards from '@/components/screener/StrategyCards';
import FilterSidebar from '@/components/screener/FilterSidebar';
import ResultsTable from '@/components/screener/ResultsTable';

export default function ScreenerPage() {
  const [filters, setFilters] = useState<Record<string, string | number>>({});

  const { data, isLoading, error } = useQuery({
    queryKey: ['screener', filters],
    queryFn: () => getScreener(filters),
    retry: 1,
  });

  const applyStrategy = (params: any) => setFilters(params);

  if (error) return (
    <div className="p-6 text-center text-slate-500">
      数据加载失败，请确认后端已启动
    </div>
  );

  return (
    <div className="p-6 space-y-6 max-w-[1440px] mx-auto">
      <StrategyCards onSelect={applyStrategy} />
      <div className="flex gap-6">
        <FilterSidebar filters={filters} onChange={setFilters} />
        <div className="flex-1 min-w-0">
          {isLoading ? <TableSkeleton rows={8} /> : <ResultsTable data={data} />}
        </div>
      </div>
    </div>
  );
}
