import React, { useState, useEffect } from 'react';
import { Lock, Download, ShieldCheck, AlertCircle, RefreshCw, Eye, EyeOff } from 'lucide-react';
import { FileUpload } from '../common/FileUpload';
import { CapacityMeter } from './CapacityMeter';
import { HashDisplay } from '../common/HashDisplay';
import { EduCard } from '../common/EduCard';
import { api } from '../../services/api';
import type { CapacityData, EncodeResponse } from '../../types';

export const EncodeForm: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [secretMessage, setSecretMessage] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [outputFilename, setOutputFilename] = useState('');
  const [capacity, setCapacity] = useState<CapacityData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<EncodeResponse | null>(null);

  // Re-calculate capacity whenever file changes
  useEffect(() => {
    if (!file) {
      setCapacity(null);
      setResult(null);
      return;
    }

    const fetchCapacity = async () => {
      try {
        const data = await api.checkCapacity(file, secretMessage);
        setCapacity(data);
      } catch (err: any) {
        setError(err.message || 'Failed to inspect cover image.');
      }
    };

    fetchCapacity();
  }, [file]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!file) {
      setError('Please select a cover image.');
      return;
    }

    if (!secretMessage.trim()) {
      setError('Please enter a secret message to hide.');
      return;
    }

    if (!password) {
      setError('Password is required for authenticated encryption.');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('secret_message', secretMessage);
      formData.append('password', password);
      formData.append('confirm_password', confirmPassword);
      if (outputFilename.trim()) {
        formData.append('output_filename', outputFilename.trim());
      }

      const res = await api.encodeMessage(formData);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to encode secret message.');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFile(null);
    setSecretMessage('');
    setPassword('');
    setConfirmPassword('');
    setOutputFilename('');
    setResult(null);
    setError(null);
    setCapacity(null);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <EduCard
        title="Why Cryptography Must Precede Steganography"
        category="Cryptographic Steganography"
        takeaway="Never store plaintext inside an image. Encryption turns meaningful patterns into pseudo-random noise, maximizing resistance to statistical steganalysis."
      >
        <p>
          Embedding unencrypted ASCII text directly into image LSBs creates distinct statistical frequency biases that signature and Chi-Square detectors immediately catch. StegoVault executes <strong>AES-256-GCM</strong> authenticated encryption with <strong>PBKDF2-HMAC-SHA256</strong> key derivation, ensuring the embedded bitstream appears mathematically indistinguishable from random sensor noise.
        </p>
      </EduCard>

      {!result ? (
        <form onSubmit={handleSubmit} className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur space-y-6">
          {/* Cover Image Upload */}
          <FileUpload
            onFileSelect={setFile}
            selectedFile={file}
            label="1. Cover Image (Lossless PNG or BMP)"
          />

          {/* Live Capacity Meter */}
          <CapacityMeter
            capacity={capacity}
            messageLength={new TextEncoder().encode(secretMessage).length}
          />

          {/* Secret Message Input */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                2. Secret Plaintext Message
              </label>
              <span className="text-xs font-mono text-slate-500">
                {new TextEncoder().encode(secretMessage).length} bytes
              </span>
            </div>
            <textarea
              rows={5}
              value={secretMessage}
              onChange={(e) => setSecretMessage(e.target.value)}
              placeholder="Enter confidential message, cryptographic keys, or sensitive dispatches..."
              className="w-full rounded-xl border border-slate-800 bg-slate-950 p-3.5 text-sm text-slate-100 placeholder-slate-600 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 font-mono resize-y"
            />
          </div>

          {/* Password & Confirmation */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
                3. Encryption Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter strong encryption password"
                  className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-sm text-slate-100 placeholder-slate-600 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
                4. Confirm Password
              </label>
              <input
                type={showPassword ? 'text' : 'password'}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm password"
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-sm text-slate-100 placeholder-slate-600 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
              />
            </div>
          </div>

          {/* Output Filename */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
              5. Output Filename (Optional)
            </label>
            <input
              type="text"
              value={outputFilename}
              onChange={(e) => setOutputFilename(e.target.value)}
              placeholder="stegovault_encoded.png"
              className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-sm text-slate-100 placeholder-slate-600 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 font-mono"
            />
          </div>

          {error && (
            <div className="flex items-center gap-2 rounded-xl border border-rose-500/30 bg-rose-950/30 p-3.5 text-sm text-rose-300">
              <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" />
              <span>{error}</span>
            </div>
          )}

          {/* Action Button */}
          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={loading || !file || !secretMessage.trim() || !password}
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-600 to-emerald-600 px-6 py-3 text-sm font-bold text-slate-950 transition-all duration-200 hover:from-cyan-500 hover:to-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg glow-cyan"
            >
              {loading ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  <span>Deriving Keys & Embedding...</span>
                </>
              ) : (
                <>
                  <Lock className="h-4 w-4 text-slate-950" />
                  <span>Encrypt & Hide in Image</span>
                </>
              )}
            </button>
          </div>
        </form>
      ) : (
        /* Result Success Card */
        <div className="rounded-2xl border border-emerald-500/40 bg-slate-900/80 p-6 backdrop-blur space-y-6 shadow-xl glow-emerald">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-emerald-500/10 p-2.5 text-emerald-400">
                <ShieldCheck className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Steganographic Embedding Succeeded</h3>
                <p className="text-xs text-slate-400">
                  Payload encrypted with AES-256-GCM and losslessly embedded into LSB bit plane.
                </p>
              </div>
            </div>

            <a
              href={result.download_url}
              download={result.output_filename}
              className="flex items-center gap-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 px-4 py-2.5 text-sm font-bold text-slate-950 transition-colors shadow"
            >
              <Download className="h-4 w-4" />
              <span>Download Stego Image</span>
            </a>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 font-mono text-xs">
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-500 text-[10px] uppercase">Output File</span>
              <p className="font-bold text-slate-200 mt-1 truncate">{result.output_filename}</p>
            </div>
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-500 text-[10px] uppercase">Payload Size</span>
              <p className="font-bold text-cyan-400 mt-1">{result.payload_bytes} bytes</p>
            </div>
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-500 text-[10px] uppercase">Dimensions</span>
              <p className="font-bold text-slate-200 mt-1">{result.dimensions} ({result.mode})</p>
            </div>
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-500 text-[10px] uppercase">Capacity Used</span>
              <p className="font-bold text-emerald-400 mt-1">{result.capacity_utilization}%</p>
            </div>
          </div>

          {/* Cryptographic Hashes */}
          <div className="space-y-3">
            <HashDisplay
              label="Original Cover Image SHA-256"
              sha256={result.cover_sha256}
            />
            <HashDisplay
              label="Generated Stego Image SHA-256"
              sha256={result.stego_sha256}
            />
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={resetForm}
              className="text-xs font-semibold text-slate-400 hover:text-cyan-400 transition-colors"
            >
              ← Encode Another Message
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
