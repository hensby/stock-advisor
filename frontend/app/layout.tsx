import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Navbar from '@/components/layout/Navbar';
import Sidebar from '@/components/layout/Sidebar';
import MobileBottomNav from '@/components/layout/MobileBottomNav';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'StockAdvisor — 美股选股与交易建议',
  description: '技术指标 + 机构情绪 + YouTube 情绪的综合评分选股平台',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className={`${inter.className} antialiased bg-[hsl(var(--background))]`}>
        <Providers>
          <div className="flex flex-col min-h-screen">
            <Navbar />
            <div className="flex flex-1 pb-16 md:pb-0">
              <Sidebar />
              <main className="flex-1 bg-slate-50/50 overflow-x-hidden">{children}</main>
            </div>
            <MobileBottomNav />
          </div>
        </Providers>
      </body>
    </html>
  );
}
