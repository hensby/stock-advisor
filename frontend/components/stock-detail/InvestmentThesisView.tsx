import { ThumbsUp, ThumbsDown } from 'lucide-react';

export default function InvestmentThesisView({ thesis, bullReasons, bearReasons }: { thesis?: string; bullReasons: string[]; bearReasons: string[] }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="bg-white shadow-card rounded-xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <ThumbsUp className="w-4 h-4 text-emerald-400" />
          <h3 className="text-sm font-medium">做多理由</h3>
        </div>
        <ul className="space-y-1.5">
          {bullReasons.length ? bullReasons.map((r, i) => (
            <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
              <span className="text-emerald-400 mt-0.5">✓</span> {r}
            </li>
          )) : <li className="text-sm text-muted-foreground">暂无</li>}
        </ul>
      </div>
      <div className="bg-white shadow-card rounded-xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <ThumbsDown className="w-4 h-4 text-red-400" />
          <h3 className="text-sm font-medium">风险因素</h3>
        </div>
        <ul className="space-y-1.5">
          {bearReasons.length ? bearReasons.map((r, i) => (
            <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
              <span className="text-red-400 mt-0.5">✗</span> {r}
            </li>
          )) : <li className="text-sm text-muted-foreground">暂无</li>}
        </ul>
      </div>
    </div>
  );
}
