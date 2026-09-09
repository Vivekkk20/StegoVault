import React from 'react';
import { ShieldAlert, AlertTriangle, Info, AlertOctagon, CheckCircle } from 'lucide-react';
import type { TechnicalFinding } from '../../types';

interface FindingsListProps {
  findings: TechnicalFinding[];
}

export const FindingsList: React.FC<FindingsListProps> = ({ findings }) => {
  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case 'CRITICAL':
        return {
          bg: 'bg-rose-500/15 text-rose-400 border-rose-500/30',
          icon: <AlertOctagon className="h-3.5 w-3.5 text-rose-400" />,
        };
      case 'HIGH':
        return {
          bg: 'bg-orange-500/15 text-orange-400 border-orange-500/30',
          icon: <AlertTriangle className="h-3.5 w-3.5 text-orange-400" />,
        };
      case 'MEDIUM':
        return {
          bg: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
          icon: <AlertTriangle className="h-3.5 w-3.5 text-amber-400" />,
        };
      case 'LOW':
        return {
          bg: 'bg-cyan-500/15 text-cyan-400 border-cyan-500/30',
          icon: <Info className="h-3.5 w-3.5 text-cyan-400" />,
        };
      default:
        return {
          bg: 'bg-slate-800 text-slate-300 border-slate-700',
          icon: <Info className="h-3.5 w-3.5 text-slate-400" />,
        };
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <ShieldAlert className="h-4 w-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            Forensic Technical Findings ({findings.length})
          </h3>
        </div>
      </div>

      {findings.length === 0 ? (
        <div className="mt-4 flex items-center gap-3 rounded-lg bg-slate-950 p-4 border border-slate-800 text-xs text-slate-400">
          <CheckCircle className="h-5 w-5 text-emerald-400" />
          <span>No anomalous technical findings were identified during the forensic analysis.</span>
        </div>
      ) : (
        <div className="mt-4 space-y-3">
          {findings.map((finding, idx) => {
            const badge = getSeverityBadge(finding.severity);
            return (
              <div
                key={idx}
                className="rounded-xl border border-slate-800/90 bg-slate-950 p-4 transition-all hover:border-slate-700"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span
                      className={`inline-flex items-center gap-1 rounded border px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider ${badge.bg}`}
                    >
                      {badge.icon}
                      {finding.severity}
                    </span>
                    <h4 className="text-sm font-bold text-slate-100">{finding.title}</h4>
                  </div>
                  <span className="text-[10px] font-mono uppercase text-slate-500 bg-slate-900 px-2 py-0.5 rounded">
                    {finding.category}
                  </span>
                </div>

                <p className="mt-2 text-xs leading-relaxed text-slate-300">
                  {finding.description}
                </p>

                {finding.evidence && (
                  <div className="mt-3 rounded bg-slate-900/90 px-3 py-2 border border-slate-800/80 font-mono text-[11px] text-cyan-300 break-all">
                    <span className="text-slate-500 font-sans font-semibold text-[10px] uppercase block mb-0.5">
                      Technical Evidence:
                    </span>
                    {finding.evidence}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
