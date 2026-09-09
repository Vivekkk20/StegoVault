import React, { useState, useEffect } from 'react';
import { Unlock, ShieldCheck, AlertCircle, RefreshCw, Copy, Check, Eye, EyeOff, CheckCircle2 } from 'lucide-react';
import { FileUpload } from '../common/FileUpload';
import { HashDisplay } from '../common/HashDisplay';
import { EduCard } from '../common/EduCard';
import { api } from '../../services/api';
import type { DecodeResponse, DetectionResponse } from '../../types';

export const DecodeForm: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [detection, setDetection] = useState<DetectionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [probing, setProbing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DecodeResponse | null>(null);
  const [copied, setCopied] = useState(false);

  // Auto-probe for StegoVault payload when file is uploaded
  useEffect(() => {
    if (!file) {
      setDetection(null);
      setResult(null);
      return;
    }

    const probeImage = async () => {
      setProbing(true);
      setError(null);
      try {
        const detectRes = await api.detectPayload(file);
        setDetection(detectRes);
      } catch {
        setDetection({ detected: false });
      } finally {
        setProbing(false);
      }
    };

    probeImage();
  }, [file]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!file) {
      setError('Please select a stego image to decode.');
      return;
    }

    if (!password) {
      setError('Password is required to decrypt the hidden message.');
      return;
    }

    setLoading(true);
    try {
      const res = await api.decodeMessage(file, password);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Unable to decode payload. Verify your password and image integrity.');
    } finally {
      setLoading(false);
    }
  };

  const copyMessage = () => {
    if (!result) return;
    navigator.clipboard.writeText(result.secret_message);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const reset = () => {
    setFile(null);
    setPassword('');
    setResult(null);
    setError(null);
    setDetection(null);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <EduCard
        title="Authenticated Decryption & Tamper Prevention"
        category="Forensic Integrity"
        takeaway="AES-256-GCM uses a 128-bit authentication tag. If even a single pixel bit is modified in transit, or if an incorrect password is used, decryption aborts immediately without exposing partial plaintext."
      >
        <p>
          Traditional unauthenticated ciphers (like AES in CBC or CTR mode) are vulnerable to bit-flipping attacks where adversaries can modify decrypted plaintext without knowing the key. StegoVault binds the binary header, salt, nonce, and ciphertext cryptographically with an authentication tag, guaranteeing confidentiality, authenticity, and non-repudiation.
        </p>
      </EduCard>

      {!result ? (
        <form onSubmit={handleSubmit} className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur space-y-6">
          {/* File Upload */}
          <FileUpload
            onFileSelect={setFile}
            selectedFile={file}
            label="1. Stego Image File (Lossless PNG or BMP)"
          />

          {/* StegoVault Payload Detection Banner */}
          {file && (
            <div className="rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-xs">
              <div className="flex items-center justify-between">
                <span className="text-slate-400 uppercase text-[10px]">Header Signature Probe</span>
                {probing ? (
                  <span className="text-cyan-400 flex items-center gap-1.5">
                    <RefreshCw className="h-3 w-3 animate-spin" /> Scanning LSBs...
                  </span>
                ) : detection?.detected ? (
                  <span className="text-emerald-400 font-bold flex items-center gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5" /> StegoVault Container Detected
                  </span>
                ) : (
                  <span className="text-slate-500">No StegoVault signature detected</span>
                )}
              </div>

              {detection?.detected && (
                <div className="mt-3 grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-slate-800/80 text-[11px]">
                  <div>
                    <span className="text-slate-500">Format Version:</span>
                    <p className="text-slate-200 font-bold">v{detection.version}</p>
                  </div>
                  <div>
                    <span className="text-slate-500">Payload Length:</span>
                    <p className="text-cyan-400 font-bold">{detection.total_payload_bytes} bytes</p>
                  </div>
                  <div>
                    <span className="text-slate-500">Header CRC32:</span>
                    <p className="text-emerald-400 font-bold">
                      {detection.header_crc_valid ? 'Valid' : 'Corrupted'}
                    </p>
                  </div>
                  <div>
                    <span className="text-slate-500">Compression:</span>
                    <p className="text-slate-200 font-bold">{detection.compressed ? 'zlib' : 'none'}</p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Password Input */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
              2. Decryption Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password used during encoding"
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

          {error && (
            <div className="rounded-xl border border-rose-500/30 bg-rose-950/30 p-4 text-xs text-rose-300 space-y-2">
              <div className="flex items-center gap-2 font-bold text-rose-400">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <span>Unable to decode payload.</span>
              </div>
              <p>{error}</p>
              <div className="pt-2 border-t border-rose-500/20 text-[11px] text-slate-400">
                <strong>Possible causes:</strong>
                <ul className="list-disc list-inside mt-1 space-y-0.5">
                  <li>Incorrect decryption password</li>
                  <li>Image was compressed with lossy formats (JPEG/WebP) after encoding</li>
                  <li>Pixel LSB bits were modified or corrupted</li>
                  <li>Image does not contain a StegoVault payload</li>
                </ul>
              </div>
            </div>
          )}

          {/* Action Button */}
          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={loading || !file || !password}
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-600 to-emerald-600 px-6 py-3 text-sm font-bold text-slate-950 transition-all duration-200 hover:from-cyan-500 hover:to-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg glow-cyan"
            >
              {loading ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  <span>Extracting & Authenticating...</span>
                </>
              ) : (
                <>
                  <Unlock className="h-4 w-4 text-slate-950" />
                  <span>Extract & Decrypt Payload</span>
                </>
              )}
            </button>
          </div>
        </form>
      ) : (
        /* Decoded Plaintext Result Card */
        <div className="rounded-2xl border border-emerald-500/40 bg-slate-900/80 p-6 backdrop-blur space-y-6 shadow-xl glow-emerald">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-emerald-500/10 p-2.5 text-emerald-400">
                <ShieldCheck className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Payload Decrypted Successfully</h3>
                <p className="text-xs text-slate-400">
                  AES-256-GCM authentication verified. SHA-256 container checksum validated.
                </p>
              </div>
            </div>

            <button
              onClick={copyMessage}
              className="flex items-center gap-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 px-4 py-2 text-sm font-bold text-slate-950 transition-colors shadow"
            >
              {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
              <span>{copied ? 'Copied to Clipboard' : 'Copy Secret Message'}</span>
            </button>
          </div>

          {/* Message Viewer */}
          <div>
            <div className="flex items-center justify-between text-xs text-slate-400 mb-2 font-mono">
              <span>DECRYPTED PLAINTEXT</span>
              <span>{result.secret_message.length} characters • {result.payload_bytes} bytes payload</span>
            </div>
            <div className="relative rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-sm text-slate-100 whitespace-pre-wrap max-h-96 overflow-y-auto leading-relaxed selection:bg-cyan-500 selection:text-slate-950">
              {result.secret_message}
            </div>
          </div>

          {/* Stego Image Hash */}
          <HashDisplay
            label="Verified Stego Image SHA-256"
            sha256={result.stego_sha256}
          />

          <div className="flex justify-end pt-2">
            <button
              onClick={reset}
              className="text-xs font-semibold text-slate-400 hover:text-cyan-400 transition-colors"
            >
              ← Decode Another Image
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
