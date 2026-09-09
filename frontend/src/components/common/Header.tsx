import { BookOpen } from 'lucide-react';
import { useEducational } from '../../context/EducationalContext';

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export const Header: React.FC<HeaderProps> = ({ title, subtitle }) => {
  const { isEduMode, toggleEduMode } = useEducational();

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-800/80 bg-slate-950/80 px-8 backdrop-blur">
      <div>
        <h2 className="text-base font-bold text-white tracking-wide">{title}</h2>
        {subtitle && <p className="text-xs text-slate-400">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-4">
        {/* System Status */}
        <div className="flex items-center gap-2 rounded-full border border-slate-800 bg-slate-900/90 px-3 py-1 text-xs">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="font-mono text-[11px] text-slate-300">SYSTEM SECURE</span>
        </div>

        {/* Educational Mode Toggle */}
        <button
          onClick={toggleEduMode}
          className={`flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-semibold transition-all duration-200 ${
            isEduMode
              ? 'border-cyan-500/50 bg-cyan-950/40 text-cyan-300 shadow-sm glow-cyan'
              : 'border-slate-800 bg-slate-900 text-slate-400 hover:text-slate-200'
          }`}
          title="Toggle Educational Explanations"
        >
          <BookOpen className={`h-3.5 w-3.5 ${isEduMode ? 'text-cyan-400' : 'text-slate-500'}`} />
          <span>Educational Mode:</span>
          <span className={`font-mono font-bold ${isEduMode ? 'text-cyan-300' : 'text-slate-500'}`}>
            {isEduMode ? 'ON' : 'OFF'}
          </span>
        </button>
      </div>
    </header>
  );
};
