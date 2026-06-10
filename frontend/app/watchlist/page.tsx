'use client';
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getWatchlists, createWatchlist, deleteWatchlist, addToWatchlist, removeFromWatchlist } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { SIGNAL_LABELS, SIGNAL_COLORS } from '@/lib/constants';
import { Plus, Trash2 } from 'lucide-react';
import Link from 'next/link';

export default function WatchlistPage() {
  const queryClient = useQueryClient();
  const [newName, setNewName] = useState('');
  const { data: watchlists, isLoading } = useQuery({ queryKey: ['watchlists'], queryFn: getWatchlists });

  const createMutation = useMutation({
    mutationFn: createWatchlist,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['watchlists'] }); setNewName(''); },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteWatchlist,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['watchlists'] }),
  });

  if (isLoading) return <div className="p-6 text-muted-foreground">加载中...</div>;

  return (
    <div className="p-6 space-y-6 max-w-[1440px] mx-auto">
      <div className="flex items-center gap-3">
        <h1 className="text-lg font-bold">自选股</h1>
        <div className="flex items-center gap-2">
          <Input placeholder="新建分组..." value={newName} onChange={e => setNewName(e.target.value)}
            className="h-8 w-40 text-sm" />
          <Button size="sm" onClick={() => newName && createMutation.mutate(newName)} disabled={!newName}><Plus className="w-3 h-3 mr-1" /> 新建</Button>
        </div>
      </div>
      {!watchlists?.length ? (
        <div className="text-sm text-muted-foreground py-8">暂无自选股分组，请创建</div>
      ) : (
        watchlists.map(wl => (
          <div key={wl.id} className="bg-white shadow-card rounded-xl overflow-hidden">
            <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
              <h2 className="text-sm font-medium">{wl.name} <span className="text-muted-foreground">({wl.item_count})</span></h2>
              <Button variant="ghost" size="sm" onClick={() => deleteMutation.mutate(wl.id)}><Trash2 className="w-3 h-3" /></Button>
            </div>
            {wl.stocks.length ? (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-slate-100 text-xs text-muted-foreground">
                      <th className="text-left px-4 py-2 font-medium">股票</th>
                      <th className="text-right px-4 py-2 font-medium">综合评分</th>
                      <th className="text-right px-4 py-2 font-medium">信号</th>
                    </tr>
                  </thead>
                  <tbody>
                    {wl.stocks.map(s => (
                      <tr key={s.ticker} className="border-b border-slate-100/50 hover:bg-accent/50">
                        <td className="px-4 py-2.5">
                          <Link href={`/stock/${s.ticker}`} className="font-medium hover:text-primary">{s.ticker}</Link>
                          <span className="text-muted-foreground ml-1.5">{s.name}</span>
                        </td>
                        <td className="px-4 py-2.5 text-right number-font">{s.composite_score?.toFixed(0) || '--'}</td>
                        <td className="px-4 py-2.5 text-right">
                          <span className={`px-2 py-0.5 rounded text-xs border ${SIGNAL_COLORS[s.signal || '']}`}>
                            {SIGNAL_LABELS[s.signal || ''] || s.signal}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="px-4 py-6 text-sm text-muted-foreground text-center">暂无股票，在筛选器中添加</div>
            )}
          </div>
        ))
      )}
    </div>
  );
}
