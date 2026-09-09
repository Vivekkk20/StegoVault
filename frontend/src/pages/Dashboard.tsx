import { useState, useEffect } from 'react';
import {
  Lock,
  Unlock,
  ScanEye,
  FileText,
  ShieldCheck,
  ArrowRight,
  Sparkles,
} from 'lucide-react';
import { EduCard } from '../components/common/EduCard';
import { api } from '../services/api';
import type { ReportSummary } from '../types';

interface DashboardProps {
  onNavigate: (tab: string, reportId?: string) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ onNavigate }) => {
  const [recentReports, setRecentReports] = useState<ReportSummary[]>([]);
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    api.listReports().then(res => setRecentReports(res.slice(0, 5))).catch(() => {});
    api.getHealth().then(setHealth).catch(() => {});
  }, []);

  const getRiskBadge = (score: number, level: string) => {
    let color = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    if (score > 60) color = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
    else if (score > 40) color = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    else if (score > 20) color = 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30';

    return (
      <span className={`inline-flex items-center rounded border px-2 py-0.5 text-[10px] font-bold uppercase font-mono ${color}`}>
        {score}/100 • {level.replace('_', ' ')}
      </span>
    );
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Hero Welcome */}
      <div className="relative overflow-hidden rounded-2xl border border-slate-800 bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 p-8 shadow-2xl">
        <div className="relative z-10 max-w-2xl space-y-3">
          <div className="inline-flex items-center gap-2 rounded-full border border-cyan-500/30 bg-cyan-950/40 px-3 py-1 text-xs text-cyan-300">
            <Sparkles className="h-3.5 w-3.5 text-cyan-400" />
            <span>Cybersecurity Forensics & Cryptographic Data Hiding Platform</span>
          </div>
          <h2 className="text-3xl font-black tracking-tight text-white sm:text-4xl">
            Secure Steganography & Steganalysis Lab
          </h2>
          <p className="text-sm leading-relaxed text-slate-400">
            StegoVault provides authenticated, losslessly embedded steganography alongside statistical forensics: multi-layer Shannon entropy, Chi-Square Pair-of-Values attacks, LSB plane distributions, trailing binary detection, and automated risk scoring.
          </p>
        </div>
      </div>

      {/* Educational Banner */}
      <EduCard
        title="What is Steganography vs. Cryptography?"
        category="Foundational Concepts"
        takeaway="Cryptography conceals the meaning of a secret message; steganography conceals the very existence of the communication. Combining both yields true plausible deniability."
      >
        <p>
          While an encrypted file flags suspicion to network defenders, embedding the ciphertext into the least-significant bits of a routine PNG or BMP image hides both the message contents and the transmission event. StegoVault couples AES-256-GCM with statistical steganalysis engines to rigorously test both data hiding and forensic detection.
        </p>
      </EduCard>

      {/* Core Workflow Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Encode */}
        <div
          onClick={() => onNavigate('encode')}
          className="group cursor-pointer rounded-2xl border border-slate-800/80 bg-slate-900/60 p-6 transition-all duration-300 hover:border-cyan-500/40 hover:bg-slate-900/90 hover:shadow-xl hover:glow-cyan"
        >
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400 group-hover:scale-110 transition-transform">
            <Lock className="h-6 w-6" />
          </div>
          <h3 className="mt-4 text-base font-bold text-white flex items-center justify-between">
            <span>Encode & Hide</span>
            <ArrowRight className="h-4 w-4 text-slate-600 group-hover:text-cyan-400 transition-colors" />
          </h3>
          <p className="mt-2 text-xs leading-relaxed text-slate-400">
            Encrypt plaintext messages with AES-256-GCM and hide into image LSB channels with zero visual degradation.
          </p>
        </div>

        {/* Decode */}
        <div
          onClick={() => onNavigate('decode')}
          className="group cursor-pointer rounded-2xl border border-slate-800/80 bg-slate-900/60 p-6 transition-all duration-300 hover:border-emerald-500/40 hover:bg-slate-900/90 hover:shadow-xl hover:glow-emerald"
        >
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400 group-hover:scale-110 transition-transform">
            <Unlock className="h-6 w-6" />
          </div>
          <h3 className="mt-4 text-base font-bold text-white flex items-center justify-between">
            <span>Decode & Decrypt</span>
            <ArrowRight className="h-4 w-4 text-slate-600 group-hover:text-emerald-400 transition-colors" />
          </h3>
          <p className="mt-2 text-xs leading-relaxed text-slate-400">
            Extract StegoVault containers, verify cryptographic checksums, and decrypt authenticated plaintext.
          </p>
        </div>

        {/* Analyzer */}
        <div
          onClick={() => onNavigate('analyzer')}
          className="group cursor-pointer rounded-2xl border border-slate-800/80 bg-slate-900/60 p-6 transition-all duration-300 hover:border-amber-500/40 hover:bg-slate-900/90 hover:shadow-xl hover:glow-amber"
        >
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-amber-500/10 text-amber-400 group-hover:scale-110 transition-transform">
            <ScanEye className="h-6 w-6" />
          </div>
          <h3 className="mt-4 text-base font-bold text-white flex items-center justify-between">
            <span>Forensic Analyzer</span>
            <ArrowRight className="h-4 w-4 text-slate-600 group-hover:text-amber-400 transition-colors" />
          </h3>
          <p className="mt-2 text-xs leading-relaxed text-slate-400">
            Audit suspicious images using Shannon entropy, Chi-Square PoV tests, trailing byte detection, and risk scoring.
          </p>
        </div>
      </div>

      {/* Security Architecture Specs */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 mb-4 flex items-center gap-2">
          <ShieldCheck className="h-4 w-4 text-emerald-400" />
          <span>Security Architecture & Cryptographic Parameters</span>
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 font-mono text-xs">
          <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
            <span className="text-slate-500 text-[10px] uppercase">Cipher Primitive</span>
            <p className="font-bold text-slate-200 mt-1">AES-256-GCM</p>
            <span className="text-[10px] text-emerald-400 font-sans">128-bit Auth Tag</span>
          </div>
          <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
            <span className="text-slate-500 text-[10px] uppercase">Key Derivation</span>
            <p className="font-bold text-slate-200 mt-1">PBKDF2-HMAC-SHA256</p>
            <span className="text-[10px] text-cyan-400 font-sans">{health?.security?.pbkdf2_iterations?.toLocaleString() || '600,000'} Iterations</span>
          </div>
          <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
            <span className="text-slate-500 text-[10px] uppercase">Integrity Hashes</span>
            <p className="font-bold text-slate-200 mt-1">SHA-256 & SHA-512</p>
            <span className="text-[10px] text-slate-400 font-sans">Header CRC32 Check</span>
          </div>
          <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
            <span className="text-slate-500 text-[10px] uppercase">Steganography Spec</span>
            <p className="font-bold text-slate-200 mt-1">Lossless RGB LSB</p>
            <span className="text-[10px] text-slate-400 font-sans">PNG & BMP formats</span>
          </div>
        </div>
      </div>

      {/* Recent Analysis Reports */}
      {recentReports.length > 0 && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <FileText className="h-4 w-4 text-cyan-400" />
              <span>Recent Forensic Analyses</span>
            </h3>
            <button
              onClick={() => onNavigate('reports')}
              className="text-xs text-cyan-400 hover:underline font-semibold"
            >
              View All Reports →
            </button>
          </div>

          <div className="divide-y divide-slate-800/80">
            {recentReports.map((rep: ReportSummary) => (
              <div
                key={rep.analysis_id}
                onClick={() => onNavigate('reports', rep.analysis_id)}
                className="flex items-center justify-between py-3 cursor-pointer hover:bg-slate-800/30 px-2 rounded-lg transition-colors"
              >
                <div>
                  <h4 className="text-sm font-semibold text-slate-200">{rep.filename}</h4>
                  <p className="text-xs text-slate-500 font-mono">
                    {new Date(rep.timestamp).toLocaleString()} • {rep.file_size_kb} KB ({rep.format})
                  </p>
                </div>
                <div>{getRiskBadge(rep.risk_score, rep.risk_level)}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
