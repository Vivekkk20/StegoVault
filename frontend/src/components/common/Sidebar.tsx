import React from 'react';
import {
  LayoutDashboard,
  Lock,
  Unlock,
  ScanEye,
  FileText,
  Settings as SettingsIcon,
  Info,
  Shield,
} from 'lucide-react';

interface SidebarProps {
  currentTab: string;
  onSelectTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, onSelectTab }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'encode', label: 'Encode & Hide', icon: Lock },
    { id: 'decode', label: 'Decode & Decrypt', icon: Unlock },
    { id: 'analyzer', label: 'Forensic Analyzer', icon: ScanEye },
    { id: 'reports', label: 'Analysis Reports', icon: FileText },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
    { id: 'about', label: 'About & Threat Model', icon: Info },
  ];

  return (
    <aside className="w-64 shrink-0 border-r border-slate-800/80 bg-slate-950 flex flex-col justify-between min-h-screen">
      <div>
        {/* Brand */}
        <div className="flex items-center gap-3 px-6 py-6 border-b border-slate-800/60">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-600 to-emerald-500 shadow-lg glow-cyan">
            <Shield className="h-5 w-5 text-slate-950" />
          </div>
          <div>
            <h1 className="text-lg font-black tracking-tight text-white flex items-center gap-1.5">
              Stego<span className="text-cyan-400">Vault</span>
            </h1>
            <span className="text-[10px] uppercase font-bold tracking-widest text-slate-500">
              Cyber Forensics
            </span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectTab(item.id)}
                className={`flex w-full items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
                }`}
              >
                <Icon className={`h-4 w-4 ${isActive ? 'text-cyan-400' : 'text-slate-500'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-900 text-xs text-slate-500">
        <div className="flex items-center justify-between font-mono text-[10px]">
          <span>ENGINE: AES-256-GCM</span>
          <span className="text-emerald-400 font-bold">ACTIVE</span>
        </div>
        <div className="mt-1 text-[10px] text-slate-600">
          Forensic Lab v1.0.0
        </div>
      </div>
    </aside>
  );
};
