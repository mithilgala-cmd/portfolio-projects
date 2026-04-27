"use client";

import { Activity, LayoutDashboard, Settings, Wallet, BarChart3, TrendingUp } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard },
    { name: "Market Data", href: "#", icon: BarChart3 },
    { name: "Bot Builder", href: "/bot-builder", icon: Settings },
    { name: "Portfolio", href: "/portfolio", icon: Wallet },
    { name: "Analytics", href: "#", icon: TrendingUp },
  ];

  return (
    <aside className="w-64 border-r border-border bg-panel/30 backdrop-blur-xl flex flex-col hidden md:flex h-full relative z-20">
      <div className="p-8">
        <h1 className="text-2xl font-black text-white flex items-center gap-2 tracking-tighter">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center shadow-[0_0_15px_rgba(59,130,246,0.5)]">
            <Activity size={20} className="text-white" />
          </div>
          ANTIGRAVITY<span className="text-primary">.</span>
        </h1>
      </div>
      
      <div className="px-4 py-2 text-[10px] font-bold text-gray-500 uppercase tracking-widest">
        Main Menu
      </div>
      
      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group ${
                isActive
                  ? "bg-primary text-white shadow-lg shadow-primary/20"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <item.icon size={20} className={isActive ? "text-white" : "group-hover:text-primary transition-colors"} />
              <span className="font-medium">{item.name}</span>
              {isActive && (
                <div className="ml-auto w-1.5 h-1.5 bg-white rounded-full" />
              )}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 mt-auto">
        <div className="p-4 bg-primary/5 border border-primary/20 rounded-2xl">
          <div className="text-xs font-bold text-primary mb-1 uppercase tracking-wider">Trading Power</div>
          <div className="flex items-center gap-2">
            <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
              <div className="w-[85%] h-full bg-primary" />
            </div>
            <span className="text-[10px] font-bold text-gray-400">85%</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
