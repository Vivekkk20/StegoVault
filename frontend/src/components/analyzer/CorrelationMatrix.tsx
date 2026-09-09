import React from 'react';
import { GitCompare, AlertTriangle } from 'lucide-react';
import type { ChannelCorrelation } from '../../types';

interface CorrelationMatrixProps {
  correlation: ChannelCorrelation;
}

export const CorrelationMatrix: React.FC<CorrelationMatrixProps> = ({ correlation }) => {
  const getCorrelationColor = (val: number, isLsb: boolean = false) => {
    if (isLsb) {
      // In LSBs, correlation near 0 is normal for independent channels, but complete 0.000 across all is noise
      return Math.abs(val) < 0.01 ? 'text-amber-400' : 'text-slate-300';
    }
    // In full channels, correlation > 0.70 is normal
    return val > 0.70 ? 'text-emerald-400' : 'text-rose-400';
  };

  const c = correlation.channel_correlation;
  const lsb = correlation.lsb_plane_correlation;

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <GitCompare className="h-4 w-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            Inter-Channel Pearson Correlation
          </h3>
        </div>
        {correlation.is_correlation_anomaly && (
          <span className="flex items-center gap-1 rounded bg-amber-500/10 px-2 py-0.5 text-xs font-semibold text-amber-400 border border-amber-500/30">
            <AlertTriangle className="h-3 w-3" /> Correlation Perturbation
          </span>
        )}
      </div>

      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Full Channels */}
        <div className="rounded-lg bg-slate-950 p-4 border border-slate-800/80">
          <h4 className="text-xs font-semibold uppercase text-slate-400 mb-3">
            Full Channel Correlation (r)
          </h4>
          <div className="space-y-2.5 font-mono text-xs">
            <div className="flex justify-between items-center py-1 border-b border-slate-800/60">
              <span className="text-slate-400">Red ↔ Green</span>
              <span className={`font-bold ${getCorrelationColor(c.r_vs_g)}`}>
                {c.r_vs_g.toFixed(4)}
              </span>
            </div>
            <div className="flex justify-between items-center py-1 border-b border-slate-800/60">
              <span className="text-slate-400">Red ↔ Blue</span>
              <span className={`font-bold ${getCorrelationColor(c.r_vs_b)}`}>
                {c.r_vs_b.toFixed(4)}
              </span>
            </div>
            <div className="flex justify-between items-center py-1">
              <span className="text-slate-400">Green ↔ Blue</span>
              <span className={`font-bold ${getCorrelationColor(c.g_vs_b)}`}>
                {c.g_vs_b.toFixed(4)}
              </span>
            </div>
          </div>
        </div>

        {/* LSB Planes */}
        <div className="rounded-lg bg-slate-950 p-4 border border-slate-800/80">
          <h4 className="text-xs font-semibold uppercase text-slate-400 mb-3">
            LSB Bit-Plane Correlation (r)
          </h4>
          <div className="space-y-2.5 font-mono text-xs">
            <div className="flex justify-between items-center py-1 border-b border-slate-800/60">
              <span className="text-slate-400">LSB Red ↔ Green</span>
              <span className={`font-bold ${getCorrelationColor(lsb.r_vs_g, true)}`}>
                {lsb.r_vs_g.toFixed(4)}
              </span>
            </div>
            <div className="flex justify-between items-center py-1 border-b border-slate-800/60">
              <span className="text-slate-400">LSB Red ↔ Blue</span>
              <span className={`font-bold ${getCorrelationColor(lsb.r_vs_b, true)}`}>
                {lsb.r_vs_b.toFixed(4)}
              </span>
            </div>
            <div className="flex justify-between items-center py-1">
              <span className="text-slate-400">LSB Green ↔ Blue</span>
              <span className={`font-bold ${getCorrelationColor(lsb.g_vs_b, true)}`}>
                {lsb.g_vs_b.toFixed(4)}
              </span>
            </div>
          </div>
        </div>
      </div>

      <p className="mt-3 text-xs leading-relaxed text-slate-400 bg-slate-950 p-2.5 rounded border border-slate-800/80">
        {correlation.evaluation}
      </p>
    </div>
  );
};
