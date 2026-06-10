'use client';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import type { SectorSentiment } from '@/lib/types';

export default function SentimentPulseChart({ sectors }: { sectors: SectorSentiment[] }) {
  if (!sectors.length) return (
    <div className="bg-white shadow-card rounded-xl p-4 text-sm text-muted-foreground">
      暂无行业情绪数据
    </div>
  );

  const data = sectors.map(s => ({
    sector: s.sector?.slice(0, 12) || 'Unknown',
    '机构情绪': s.institutional_avg_score ?? 0,
    'YouTube情绪': s.youtube_avg_score ?? 0,
  }));

  return (
    <div className="bg-white shadow-card rounded-xl p-4">
      <h3 className="text-sm font-medium mb-3">行业情绪对比</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 5, right: 5, bottom: 20, left: -10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis dataKey="sector" tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }} angle={-35} textAnchor="end" />
          <YAxis tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }} domain={[0, 100]} />
          <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '8px', fontSize: '12px' }} />
          <Legend wrapperStyle={{ fontSize: '12px' }} />
          <Bar dataKey="机构情绪" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          <Bar dataKey="YouTube情绪" fill="#f59e0b" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
