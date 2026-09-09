import React from 'react';
import { DecodeForm } from '../components/decode/DecodeForm';

export const DecodePage: React.FC = () => {
  return (
    <div className="space-y-6 pb-12">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white tracking-wide">
          Steganographic Extraction & Authenticated Decryption
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Extract hidden StegoVault payloads from lossless images, verify container integrity, and decrypt secret messages.
        </p>
      </div>

      <DecodeForm />
    </div>
  );
};
