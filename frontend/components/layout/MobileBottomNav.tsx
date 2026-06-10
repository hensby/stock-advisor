'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Search, FileText, Star } from 'lucide-react';

const items = [
  { href: '/', label: '仪表盘', icon: LayoutDashboard },
  { href: '/screener', label: '筛选', icon: Search },
  { href: '/briefing', label: '简报', icon: FileText },
  { href: '/watchlist', label: '自选', icon: Star },
];

export default function MobileBottomNav() {
  const pathname = usePathname();
  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200/60 flex justify-around py-2 z-50">
      {items.map(item => {
        const Icon = item.icon;
        const active = pathname === item.href;
        return (
          <Link key={item.href} href={item.href}
            className={`flex flex-col items-center gap-0.5 px-3 py-1 rounded-lg transition-colors ${
              active ? 'text-blue-600' : 'text-slate-400 hover:text-slate-600'
            }`}>
            <Icon className="w-5 h-5" />
            <span className="text-[10px] font-medium">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
