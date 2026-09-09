import { AlertTriangle, ShieldCheck, AlertOctagon } from 'lucide-react';

interface RiskMeterProps {
  score: number;
  riskLevel: string;
}

export const RiskMeter: React.FC<RiskMeterProps> = ({ score, riskLevel }) => {
  const getRiskColor = (s: number) => {
    if (s <= 20) return { bg: 'bg-emerald-500', text: 'text-emerald-400', border: 'border-emerald-500/30', glow: 'glow-emerald' };
    if (s <= 40) return { bg: 'bg-cyan-500', text: 'text-cyan-400', border: 'border-cyan-500/30', glow: 'glow-cyan' };
    if (s <= 60) return { bg: 'bg-amber-500', text: 'text-amber-400', border: 'border-amber-500/30', glow: 'glow-amber' };
    if (s <= 80) return { bg: 'bg-orange-500', text: 'text-orange-400', border: 'border-orange-500/30', glow: 'glow-amber' };
    return { bg: 'bg-rose-600', text: 'text-rose-400', border: 'border-rose-500/40', glow: 'glow-red' };
  };

  const getRiskIcon = (s: number) => {
    if (s <= 40) return <ShieldCheck className="h-6 w-6 text-emerald-400" />;
    if (s <= 60) return <AlertTriangle className="h-6 w-6 text-amber-400" />;
    return <AlertOctagon className="h-6 w-6 text-rose-400" />;
  };

  const colors = getRiskColor(score);
  const formattedLevel = riskLevel.replace('_', ' ');

  return (
    <div className={`rounded-xl border ${colors.border} bg-slate-900/90 p-5 ${colors.glow} backdrop-blur`}>
      <div className="flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Steganography Risk Score
          </span>
          <div className="mt-1 flex items-baseline gap-2">
            <span className={`text-4xl font-black tracking-tight ${colors.text}`}>
              {score}
            </span>
            <span className="text-xs font-medium text-slate-500">/ 100</span>
          </div>
        </div>
        <div className="flex flex-col items-end">
          <div className="flex items-center gap-2">
            {getRiskIcon(score)}
            <span className={`rounded-md px-2.5 py-1 text-xs font-bold uppercase tracking-wider ${colors.bg} text-slate-950`}>
              {formattedLevel}
            </span>
          </div>
        </div>
      </div>

      {/* Visual meter bar */}
      <div className="mt-4">
        <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-800">
          <div
            className={`h-full transition-all duration-700 ease-out ${colors.bg}`}
            style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
          />
        </div>
        <div className="mt-2 flex justify-between text-[10px] text-slate-500 font-mono">
          <span>0 (Very Low)</span>
          <span>40 (Low)</span>
          <span>60 (Moderate)</span>
          <span>80 (High)</span>
          <span>100 (Critical)</span>
        </div>
      </div>
    </div>
  );
};
