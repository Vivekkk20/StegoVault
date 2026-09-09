import React from 'react';
import { HardDrive, CheckCircle2, AlertOctagon } from 'lucide-react';
import type { CapacityData } from '../../types';

interface CapacityMeterProps {
  capacity: CapacityData | null;
  messageLength: number;
}

export const CapacityMeter: React.FC<CapacityMeterProps> = ({ capacity, messageLength }) => {
  if (!capacity) return null;

  const fixedOverhead = 96; // 64 bytes header + 32 bytes SHA256 trailer
  const requiredBytes = messageLength + fixedOverhead;
  const availableBytes = capacity.capacity_bytes;
  const isSufficient = availableBytes >= requiredBytes;
  const utilization = availableBytes > 0 ? (requiredBytes / availableBytes) * 100 : 0;

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-4 backdrop-blur">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-300">
          <HardDrive className="h-4 w-4 text-cyan-400" />
          <span>Image Capacity Analysis</span>
        </div>
        <span
          className={`flex items-center gap-1 rounded px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider ${
            isSufficient
              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
              : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
          }`}
        >
          {isSufficient ? (
            <>
              <CheckCircle2 className="h-3 w-3" /> Enough Capacity
            </>
          ) : (
            <>
              <AlertOctagon className="h-3 w-3" /> Insufficient Capacity
            </>
          )}
        </span>
      </div>

      <div className="mt-3 grid grid-cols-2 gap-4 text-xs font-mono">
        <div>
          <span className="text-slate-500 uppercase text-[10px]">Available Capacity</span>
          <p className="text-sm font-bold text-slate-200 mt-0.5">
            {capacity.capacity_kb} KB <span className="text-xs text-slate-500">({availableBytes.toLocaleString()} B)</span>
          </p>
        </div>
        <div>
          <span className="text-slate-500 uppercase text-[10px]">Required Payload</span>
          <p className="text-sm font-bold text-cyan-400 mt-0.5">
            {(requiredBytes / 1024).toFixed(2)} KB <span className="text-xs text-slate-500">({requiredBytes.toLocaleString()} B)</span>
          </p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mt-3">
        <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
          <div
            className={`h-full transition-all duration-300 ${
              isSufficient ? (utilization > 80 ? 'bg-amber-400' : 'bg-cyan-500') : 'bg-rose-500'
            }`}
            style={{ width: `${Math.min(100, utilization)}%` }}
          />
        </div>
        <div className="mt-1.5 flex justify-between text-[10px] text-slate-500 font-mono">
          <span>0%</span>
          <span>Utilization: {utilization.toFixed(1)}%</span>
          <span>100%</span>
        </div>
      </div>
    </div>
  );
};
