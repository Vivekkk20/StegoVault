import { useState } from 'react';
import { AlertOctagon, CheckCircle2, Copy, Check } from 'lucide-react';
import type { TrailingDataInfo } from '../../types';

interface TrailingDataCardProps {
  trailing: TrailingDataInfo;
}

export const TrailingDataCard: React.FC<TrailingDataCardProps> = ({ trailing }) => {
  const [copied, setCopied] = useState(false);

  const copyHash = (text?: string) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!trailing.detected) {
    return (
      <div className="rounded-xl border border-emerald-500/20 bg-emerald-950/10 p-4 backdrop-blur flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-lg bg-emerald-500/10 p-2 text-emerald-400">
            <CheckCircle2 className="h-5 w-5" />
          </div>
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400">
              Binary Structure Integrity Verified
            </h4>
            <p className="text-xs text-slate-300 mt-0.5">
              No trailing payload or appended data detected past the legal EOF marker.
            </p>
          </div>
        </div>
        <span className="font-mono text-xs text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded border border-emerald-500/20">
          Clean EOF
        </span>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-rose-500/50 bg-rose-950/25 p-5 shadow-lg glow-red backdrop-blur">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2 text-rose-400 font-bold uppercase tracking-wider text-sm">
          <AlertOctagon className="h-5 w-5" />
          <span>⚠ Additional Trailing Data Detected Past EOF</span>
        </div>
        <span className="rounded bg-rose-500 px-2 py-0.5 text-xs font-bold uppercase text-slate-950">
          STRUCTURAL ANOMALY
        </span>
      </div>

      <p className="mt-2 text-xs leading-relaxed text-rose-200">
        {trailing.description || 'Binary data was found appended past the legal image terminal marker.'}
      </p>

      <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="rounded-lg bg-slate-950 p-2.5 border border-rose-500/20">
          <span className="text-[10px] text-slate-400 uppercase">Legal EOF Offset</span>
          <p className="font-mono text-xs font-bold text-slate-100 mt-0.5">
            {trailing.legal_eof_offset} bytes
          </p>
        </div>
        <div className="rounded-lg bg-slate-950 p-2.5 border border-rose-500/20">
          <span className="text-[10px] text-slate-400 uppercase">Appended Payload Size</span>
          <p className="font-mono text-xs font-bold text-rose-300 mt-0.5">
            {trailing.trailing_size_bytes} bytes ({trailing.trailing_size_kb} KB)
          </p>
        </div>
        <div className="rounded-lg bg-slate-950 p-2.5 border border-rose-500/20">
          <div className="flex justify-between items-center text-[10px] text-slate-400 uppercase">
            <span>Payload SHA-256</span>
            <button
              onClick={() => copyHash(trailing.sha256)}
              className="text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
            >
              {copied ? <Check className="h-2.5 w-2.5 text-emerald-400" /> : <Copy className="h-2.5 w-2.5" />}
              {copied ? 'Copied' : 'Copy'}
            </button>
          </div>
          <p className="font-mono text-[10px] text-cyan-300 truncate mt-0.5">
            {trailing.sha256}
          </p>
        </div>
      </div>

      {trailing.preview_hex && (
        <div className="mt-3">
          <span className="text-[10px] uppercase font-semibold text-slate-400">
            Hex Dump Preview (First 64 Bytes):
          </span>
          <div className="mt-1 rounded bg-slate-950 p-2 font-mono text-[11px] text-slate-300 break-all border border-slate-800">
            {trailing.preview_hex}
          </div>
        </div>
      )}
    </div>
  );
};
