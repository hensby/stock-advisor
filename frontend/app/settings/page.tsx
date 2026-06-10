'use client';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getScoringWeights, updateScoringWeights } from '@/lib/api';
import { Button } from '@/components/ui/button';
import type { ScoringWeights } from '@/lib/types';
import { useState, useEffect } from 'react';

const LABELS: { key: keyof ScoringWeights; label: string; color: string }[] = [
  { key: 'technical', label: '技术面', color: 'bg-emerald-500' },
  { key: 'institutional', label: '机构情绪', color: 'bg-blue-500' },
  { key: 'youtube', label: 'YouTube', color: 'bg-amber-500' },
  { key: 'fundamental', label: '基本面', color: 'bg-violet-500' },
];

export default function SettingsPage() {
  const queryClient = useQueryClient();
  const { data } = useQuery({ queryKey: ['weights'], queryFn: getScoringWeights });
  const [weights, setWeights] = useState<ScoringWeights | null>(null);

  useEffect(() => { if (data) setWeights(data); }, [data]);

  const mutation = useMutation({
    mutationFn: updateScoringWeights,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['weights'] }),
  });

  if (!weights) return <div className="p-6 text-muted-foreground">加载中...</div>;

  const total = LABELS.reduce((s, l) => s + (weights[l.key] || 0), 0);

  const update = (key: keyof ScoringWeights, val: number) => {
    if (!weights) return;
    setWeights({ ...weights, [key]: val });
  };

  const save = () => {
    if (Math.abs(total - 1) > 0.01) return alert('权重之和必须为 1.0');
    mutation.mutate(weights);
  };

  return (
    <div className="p-6 space-y-6 max-w-2xl">
      <div>
        <h1 className="text-lg font-bold">设置</h1>
        <p className="text-sm text-muted-foreground">调整综合评分的各项权重</p>
      </div>
      <div className="bg-white shadow-card rounded-xl p-6 space-y-4">
        {LABELS.map(({ key, label, color }) => (
          <div key={key} className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>{label}</span>
              <span className="number-font">{((weights[key] || 0) * 100).toFixed(0)}%</span>
            </div>
            <input type="range" min="0" max="100" value={(weights[key] || 0) * 100}
              onChange={e => update(key, Number(e.target.value) / 100)}
              className="w-full accent-primary" />
          </div>
        ))}
        <div className="flex items-center justify-between pt-4 border-t border-border">
          <span className="text-sm font-medium">总计</span>
          <span className={`number-font font-bold ${Math.abs(total - 1) < 0.01 ? 'text-emerald-400' : 'text-red-400'}`}>
            {(total * 100).toFixed(0)}%
          </span>
        </div>
        <Button onClick={save} disabled={Math.abs(total - 1) > 0.01 || mutation.isPending} className="w-full">
          {mutation.isPending ? '保存中...' : '保存'}
        </Button>
      </div>
    </div>
  );
}
