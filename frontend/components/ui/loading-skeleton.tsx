export function PageSkeleton() {
  return (
    <div className="p-6 space-y-6 max-w-[1440px] mx-auto animate-pulse">
      <div className="grid grid-cols-4 gap-3">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-20 bg-slate-100 rounded-xl" />
        ))}
      </div>
      <div className="h-6 w-32 bg-slate-100 rounded" />
      <div className="flex gap-3 overflow-hidden">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-32 w-48 bg-slate-100 rounded-xl shrink-0" />
        ))}
      </div>
      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 h-64 bg-slate-100 rounded-xl" />
        <div className="h-64 bg-slate-100 rounded-xl" />
      </div>
    </div>
  );
}

export function CardSkeleton() {
  return <div className="h-24 bg-slate-100 rounded-xl animate-pulse" />;
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="bg-white rounded-xl p-4 space-y-3 animate-pulse">
      <div className="h-4 w-1/4 bg-slate-100 rounded" />
      {[...Array(rows)].map((_, i) => (
        <div key={i} className="h-8 bg-slate-50 rounded" />
      ))}
    </div>
  );
}
