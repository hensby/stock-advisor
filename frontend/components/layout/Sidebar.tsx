'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Search, FileText, Star, Settings } from 'lucide-react';

const ITEMS = [
  { href: '/', label: '仪表盘', icon: LayoutDashboard },
  { href: '/screener', label: '筛选器', icon: Search },
  { href: '/briefing', label: '每日简报', icon: FileText },
  { href: '/watchlist', label: '自选股', icon: Star },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden md:flex w-56 bg-white border-r border-slate-200/60 flex flex-col shrink-0">
      <div className="flex-1 py-4 px-3 space-y-0.5">
        {ITEMS.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                active
                  ? 'bg-blue-50 text-blue-600'
                  : 'text-slate-500 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <Icon className="w-4 h-4" />
              {item.label}
            </Link>
          );
        })}
      </div>

      <div className="p-3 border-t border-slate-200/60">
        <Link
          href="/settings"
          className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
            pathname === '/settings'
              ? 'bg-blue-50 text-blue-600'
              : 'text-slate-500 hover:text-slate-900 hover:bg-slate-50'
          }`}
        >
          <Settings className="w-4 h-4" />
          设置
        </Link>
      </div>
    </aside>
  );
}
