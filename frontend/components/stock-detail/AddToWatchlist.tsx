'use client';
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getWatchlists, addToWatchlist } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Plus, Check } from 'lucide-react';

export default function AddToWatchlist({ ticker }: { ticker: string }) {
  const [open, setOpen] = useState(false);
  const [added, setAdded] = useState<number[]>([]);
  const queryClient = useQueryClient();
  const { data: watchlists } = useQuery({ queryKey: ['watchlists'], queryFn: getWatchlists });

  const mutation = useMutation({
    mutationFn: (wid: number) => addToWatchlist(wid, ticker),
    onSuccess: (_, wid) => {
      setAdded(prev => [...prev, wid]);
      queryClient.invalidateQueries({ queryKey: ['watchlists'] });
    },
  });

  if (!watchlists?.length) return null;

  return (
    <div className="relative">
      <Button variant="outline" size="sm" onClick={() => setOpen(!open)}
        className="text-slate-600 border-slate-200 hover:bg-slate-50">
        <Plus className="w-3.5 h-3.5 mr-1" />
        加入自选
      </Button>
      {open && (
        <div className="absolute right-0 top-full mt-1 w-48 bg-white rounded-xl shadow-lg border border-slate-100 py-1 z-50">
          {watchlists.map(wl => (
            <button key={wl.id}
              onClick={() => !added.includes(wl.id) && mutation.mutate(wl.id)}
              disabled={added.includes(wl.id)}
              className="w-full px-3 py-2 text-left text-sm hover:bg-slate-50 flex items-center justify-between disabled:opacity-50"
            >
              {wl.name}
              {added.includes(wl.id) && <Check className="w-3.5 h-3.5 text-emerald-500" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
