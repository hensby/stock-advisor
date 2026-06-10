import type { ScoreBreakdown } from '@/lib/types';

function ScoreBar({ label, score, color }: { label: string; score?: number; color: string }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-muted-foreground">{label}</span>
        <span className="number-font">{score != null ? score.toFixed(0) : '--'}</span>
      </div>
      <div className="w-full bg-secondary rounded-full h-1.5">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${score || 0}%` }} />
      </div>
    </div>
  );
}

export default function ScoreBreakdownView({ scores }: { scores?: ScoreBreakdown }) {
  return (
    <div className="bg-white shadow-card rounded-xl p-4">
      <h3 className="text-sm font-medium mb-3">评分分解</h3>
      <div className="space-y-3">
        <ScoreBar label="技术面" score={scores?.technical_score} color="bg-emerald-500" />
        <ScoreBar label="机构情绪" score={scores?.institutional_score} color="bg-blue-500" />
        <ScoreBar label="YouTube" score={scores?.youtube_score} color="bg-amber-500" />
        <ScoreBar label="基本面" score={scores?.fundamental_score} color="bg-violet-500" />
      </div>
      {scores?.composite_score != null && (
        <div className="mt-4 pt-3 border-t border-border">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium">综合评分</span>
            <span className="number-font text-lg font-bold">{scores.composite_score.toFixed(0)}</span>
          </div>
        </div>
      )}
    </div>
  );
}
