import { SIGNAL_LABELS, SIGNAL_COLORS } from '@/lib/constants';
import type { SignalEvent } from '@/lib/types';

export default function SignalTimeline({ history }: { history: SignalEvent[] }) {
  if (!history.length) return (
    <div className="bg-white shadow-card rounded-xl p-4 text-sm text-muted-foreground">
      暂无信号变化记录
    </div>
  );

  return (
    <div className="bg-white shadow-card rounded-xl p-4">
      <h3 className="text-sm font-medium mb-3">信号变化时间线</h3>
      <div className="space-y-0">
        {history.slice(0, 10).map((event, i) => (
          <div key={i} className="flex items-start gap-3 py-2 border-b border-slate-100/50 last:border-0">
            <div className="w-2 h-2 mt-1.5 rounded-full bg-primary shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="number-font text-xs text-muted-foreground">{event.date}</span>
                <span className={`px-1.5 py-0.5 rounded text-xs border ${SIGNAL_COLORS[event.signal || '']}`}>
                  {SIGNAL_LABELS[event.signal || ''] || event.signal}
                </span>
              </div>
              {event.trigger_reasons.length > 0 && (
                <p className="text-xs text-muted-foreground mt-1">{event.trigger_reasons.join(' · ')}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
