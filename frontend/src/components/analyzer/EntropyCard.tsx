import React from 'react';
import { Activity, AlertTriangle } from 'lucide-react';
import type { EntropyAnalysis } from '../../types';

interface EntropyCardProps {
  entropy: EntropyAnalysis;
}

export const EntropyCard: React.FC<EntropyCardProps> = ({ entropy }) => {
  const getEntropyBar = (val: number, max: number = 8.0, isLsb: boolean = false) => {
    const pct = Math.min(100, (val / max) * 100);
    const isSuspicious = isLsb && val > 0.998;
    return (
      <div className="flex items-center gap-3">
        <div className="h-2 flex-1 overflow-hidden rounded-full bg-slate-800">
          <div
            className={`h-full transition-all duration-500 ${
              isSuspicious ? 'bg-amber-400' : 'bg-cyan-500'
            }`}
            style={{ width: `${pct}%` }}
          />
        </div>
        <span className={`w-12 text-right font-mono text-xs ${isSuspicious ? 'text-amber-400 font-bold' : 'text-slate-300'}`}>
          {val.toFixed(3)}
        </span>
      </div>
    );
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Activity className="h-4 w-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            Shannon Entropy Analysis
          </h3>
        </div>
        {entropy.is_lsb_anomaly && (
          <span className="flex items-center gap-1 rounded bg-amber-500/10 px-2 py-0.5 text-xs font-semibold text-amber-400 border border-amber-500/30">
            <AlertTriangle className="h-3 w-3" /> LSB Entropy Anomaly
          </span>
        )}
      </div>

      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Macro Byte Entropy */}
        <div className="space-y-3">
          <h4 className="text-xs font-semibold uppercase text-slate-400">
            Color Channel Byte Entropy (0 - 8.0)
          </h4>
          <div className="space-y-2">
            <div>
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>Red Channel</span>
              </div>
              {getEntropyBar(entropy.channels_entropy.red || 0, 8.0)}
            </div>
            <div>
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>Green Channel</span>
              </div>
              {getEntropyBar(entropy.channels_entropy.green || 0, 8.0)}
            </div>
            <div>
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>Blue Channel</span>
              </div>
              {getEntropyBar(entropy.channels_entropy.blue || 0, 8.0)}
            </div>
            <div className="pt-2 border-t border-slate-800">
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>Raw File Entropy</span>
              </div>
              {getEntropyBar(entropy.file_entropy, 8.0)}
            </div>
          </div>
        </div>

        {/* LSB Bit-Plane Entropy */}
        <div className="space-y-3">
          <h4 className="text-xs font-semibold uppercase text-slate-400">
            LSB Bit-Plane Entropy (0 - 1.0)
          </h4>
          <div className="space-y-2">
            <div>
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>Red LSB</span>
              </div>
              {getEntropyBar(entropy.lsb_bit_entropy.red || 0, 1.0, true)}
            </div>
            <div>
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>Green LSB</span>
              </div>
              {getEntropyBar(entropy.lsb_bit_entropy.green || 0, 1.0, true)}
            </div>
            <div>
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>Blue LSB</span>
              </div>
              {getEntropyBar(entropy.lsb_bit_entropy.blue || 0, 1.0, true)}
            </div>
          </div>

          <p className="mt-3 text-xs leading-relaxed text-slate-400 bg-slate-950 p-2.5 rounded border border-slate-800/80">
            {entropy.evaluation}
          </p>
        </div>
      </div>
    </div>
  );
};
