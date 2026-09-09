import React, { useState } from 'react';
import { Copy, Check, ShieldCheck } from 'lucide-react';

interface HashDisplayProps {
  sha256: string;
  sha512?: string;
  label?: string;
}

export const HashDisplay: React.FC<HashDisplayProps> = ({ sha256, sha512, label = 'Cryptographic Fingerprint' }) => {
  const [copied256, setCopied256] = useState(false);
  const [copied512, setCopied512] = useState(false);

  const copyToClipboard = (text: string, is512: boolean) => {
    navigator.clipboard.writeText(text);
    if (is512) {
      setCopied512(true);
      setTimeout(() => setCopied512(false), 2000);
    } else {
      setCopied256(true);
      setTimeout(() => setCopied256(false), 2000);
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-4 backdrop-blur">
      <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
        <ShieldCheck className="h-4 w-4 text-emerald-400" />
        <span>{label}</span>
      </div>

      {/* SHA-256 */}
      <div className="mt-3">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span className="font-semibold text-slate-300">SHA-256</span>
          <button
            onClick={() => copyToClipboard(sha256, false)}
            className="flex items-center gap-1 text-[11px] text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            {copied256 ? <Check className="h-3 w-3 text-emerald-400" /> : <Copy className="h-3 w-3" />}
            {copied256 ? 'Copied' : 'Copy'}
          </button>
        </div>
        <div className="mt-1 font-mono text-xs text-cyan-300 break-all bg-slate-950/70 p-2 rounded border border-slate-800/80">
          {sha256}
        </div>
      </div>

      {/* Optional SHA-512 */}
      {sha512 && (
        <div className="mt-3 pt-3 border-t border-slate-800/60">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="font-semibold text-slate-300">SHA-512</span>
            <button
              onClick={() => copyToClipboard(sha512, true)}
              className="flex items-center gap-1 text-[11px] text-cyan-400 hover:text-cyan-300 transition-colors"
            >
              {copied512 ? <Check className="h-3 w-3 text-emerald-400" /> : <Copy className="h-3 w-3" />}
              {copied512 ? 'Copied' : 'Copy'}
            </button>
          </div>
          <div className="mt-1 font-mono text-[10px] text-slate-400 break-all bg-slate-950/70 p-2 rounded border border-slate-800/80 max-h-16 overflow-y-auto">
            {sha512}
          </div>
        </div>
      )}
    </div>
  );
};
