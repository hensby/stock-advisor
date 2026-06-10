'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Search, BarChart3, Settings } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { useState } from 'react';

const NAV_ITEMS = [
  { href: '/', label: '仪表盘' },
  { href: '/screener', label: '筛选器' },
  { href: '/briefing', label: '简报' },
  { href: '/watchlist', label: '自选' },
];

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [search, setSearch] = useState('');

  const handleSearch = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && search.trim()) {
      router.push(`/stock/${search.trim().toUpperCase()}`);
      setSearch('');
    }
  };

  return (
    <header className="h-14 bg-white border-b border-slate-200/60 flex items-center px-6 gap-6 shrink-0">
      <Link href="/" className="flex items-center gap-2.5 font-bold text-lg text-slate-900">
        <div className="w-7 h-7 rounded-lg bg-blue-600 flex items-center justify-center">
          <BarChart3 className="w-4 h-4 text-white" />
        </div>
        StockAdvisor
      </Link>

      <nav className="flex items-center gap-0.5 ml-2">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                active
                  ? 'bg-blue-50 text-blue-600'
                  : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="flex-1" />

      <div className="relative w-60">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
        <Input
          placeholder="搜索股票代码..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={handleSearch}
          className="pl-9 h-9 bg-slate-50 border-slate-200 text-sm rounded-lg focus:bg-white"
        />
      </div>

      <Link
        href="/settings"
        className={`p-2 rounded-lg transition-colors ${
          pathname === '/settings'
            ? 'bg-blue-50 text-blue-600'
            : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100'
        }`}
      >
        <Settings className="w-5 h-5" />
      </Link>
    </header>
  );
}
