import React from 'react';
import { BookOpen, Sparkles } from 'lucide-react';
import { useEducational } from '../../context/EducationalContext';

interface EduCardProps {
  title: string;
  category?: string;
  children: React.ReactNode;
  takeaway?: string;
}

export const EduCard: React.FC<EduCardProps> = ({ title, category = 'Forensic Theory', children, takeaway }) => {
  const { isEduMode } = useEducational();

  if (!isEduMode) return null;

  return (
    <div className="relative overflow-hidden rounded-xl border border-cyan-500/30 bg-gradient-to-br from-cyan-950/20 via-slate-900/60 to-slate-950 p-4 shadow-lg backdrop-blur transition-all duration-200 hover:border-cyan-500/50">
      <div className="flex items-start gap-3">
        <div className="mt-0.5 rounded-lg bg-cyan-500/10 p-2 text-cyan-400">
          <BookOpen className="h-5 w-5" />
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-400">
              {category}
            </span>
            <span className="inline-flex items-center gap-1 rounded bg-cyan-500/10 px-1.5 py-0.5 text-[9px] text-cyan-300">
              <Sparkles className="h-2.5 w-2.5" /> Edu Mode Active
            </span>
          </div>
          <h4 className="mt-1 text-sm font-semibold text-slate-100">{title}</h4>
          <div className="mt-2 text-xs leading-relaxed text-slate-300">{children}</div>
          {takeaway && (
            <div className="mt-3 rounded-md border border-cyan-500/20 bg-cyan-950/40 px-3 py-1.5 text-[11px] text-cyan-200">
              <span className="font-semibold text-cyan-400">Key Takeaway: </span>
              {takeaway}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
