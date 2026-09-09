import React from 'react';
import { Binary, CheckCircle2, AlertOctagon } from 'lucide-react';
import type { LSBAnalysis } from '../../types';

interface LsbAnalysisCardProps {
  lsb: LSBAnalysis;
}

export const LsbAnalysisCard: React.FC<LsbAnalysisCardProps> = ({ lsb }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Binary className="h-4 w-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            LSB Bit-Plane & Chi-Square (χ²) Analysis
          </h3>
        </div>
        <span className="text-xs text-slate-400">
          Suspicious Channels: <span className="font-bold text-cyan-400">{lsb.suspicious_channels_count}</span>
        </span>
      </div>

      <div className="mt-4 overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400">
              <th className="pb-2 font-semibold uppercase">Channel</th>
              <th className="pb-2 font-semibold uppercase">0 / 1 Bit Ratio</th>
              <th className="pb-2 font-semibold uppercase">Deviation (±50%)</th>
              <th className="pb-2 font-semibold uppercase">χ² Statistic</th>
              <th className="pb-2 font-semibold uppercase">p-Value</th>
              <th className="pb-2 font-semibold uppercase text-right">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono">
            {Object.entries(lsb.channels).map(([chName, chData]) => {
              const dist = chData.distribution;
              const chi = chData.chi_square;
              const isSuspicious = chData.status === 'Suspicious';

              return (
                <tr key={chName} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-2.5 font-bold capitalize text-slate-200">{chName}</td>
                  <td className="py-2.5 text-slate-300">
                    {dist ? `${dist.percentage_0}% / ${dist.percentage_1}%` : 'N/A'}
                  </td>
                  <td className="py-2.5 text-slate-300">
                    {dist ? `${dist.deviation_from_50.toFixed(3)}%` : 'N/A'}
                  </td>
                  <td className="py-2.5 text-slate-300">
                    {chi ? chi.chi2_statistic.toFixed(2) : 'N/A'}
                  </td>
                  <td className="py-2.5 text-slate-300">
                    {chi ? chi.p_value.toFixed(4) : 'N/A'}
                  </td>
                  <td className="py-2.5 text-right">
                    <span
                      className={`inline-flex items-center gap-1 rounded px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider ${
                        isSuspicious
                          ? 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                          : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                      }`}
                    >
                      {isSuspicious ? (
                        <AlertOctagon className="h-3 w-3" />
                      ) : (
                        <CheckCircle2 className="h-3 w-3" />
                      )}
                      {chData.status}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-4 rounded-lg bg-slate-950 p-3 text-xs text-slate-400 border border-slate-800/80 leading-relaxed">
        <span className="font-semibold text-slate-300">Forensic Summary: </span>
        {lsb.summary}
      </div>
    </div>
  );
};
