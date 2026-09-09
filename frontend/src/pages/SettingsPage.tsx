import { useState, useEffect } from 'react';
import { Shield, BookOpen, Check } from 'lucide-react';
import { useEducational } from '../context/EducationalContext';
import { api } from '../services/api';

export const SettingsPage: React.FC = () => {
  const { isEduMode, toggleEduMode } = useEducational();
  const [health, setHealth] = useState<any>(null);
  const [savedNotice, setSavedNotice] = useState(false);

  useEffect(() => {
    api.getHealth().then(setHealth).catch(() => {});
  }, []);

  const handleToggle = () => {
    toggleEduMode();
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto pb-12">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white tracking-wide">
          Application & Security Preferences
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Configure educational telemetry and review platform cryptographic parameters.
        </p>
      </div>

      {/* Educational Mode Settings */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-cyan-500/10 p-2.5 text-cyan-400">
              <BookOpen className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white">Educational Cyber Mode</h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Displays contextual forensic guidance, cryptographic explanations, and theoretical callouts across all modules.
              </p>
            </div>
          </div>

          <button
            onClick={handleToggle}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
              isEduMode ? 'bg-cyan-500' : 'bg-slate-800'
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-slate-950 transition-transform ${
                isEduMode ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </div>

        {savedNotice && (
          <div className="flex items-center gap-1.5 text-xs text-emerald-400 font-mono">
            <Check className="h-3.5 w-3.5" />
            <span>Preferences updated</span>
          </div>
        )}
      </div>

      {/* Cryptographic Security Baseline */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur space-y-4">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-3">
          <div className="rounded-xl bg-emerald-500/10 p-2.5 text-emerald-400">
            <Shield className="h-6 w-6" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">Cryptographic Standards</h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Strict parameters enforced across all steganographic containers.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 font-mono text-xs">
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-slate-500 text-[10px] uppercase">Encryption Cipher</span>
            <p className="text-slate-200 font-bold mt-1">AES-256-GCM (Authenticated)</p>
            <p className="text-[10px] text-slate-500 font-sans mt-0.5">128-bit authentication tag; zero custom ciphers.</p>
          </div>

          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-slate-500 text-[10px] uppercase">Key Derivation</span>
            <p className="text-slate-200 font-bold mt-1">PBKDF2-HMAC-SHA256</p>
            <p className="text-[10px] text-slate-500 font-sans mt-0.5">
              {health?.security?.pbkdf2_iterations?.toLocaleString() || '600,000'} iterations with 16-byte random salt.
            </p>
          </div>

          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-slate-500 text-[10px] uppercase">Integrity Verification</span>
            <p className="text-slate-200 font-bold mt-1">Header CRC32 + Payload SHA-256</p>
            <p className="text-[10px] text-slate-500 font-sans mt-0.5">Dual-layer tamper rejection.</p>
          </div>

          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-slate-500 text-[10px] uppercase">File Upload Boundary</span>
            <p className="text-slate-200 font-bold mt-1">20 MB Maximum Size</p>
            <p className="text-[10px] text-slate-500 font-sans mt-0.5">Strict magic-byte header validation.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
