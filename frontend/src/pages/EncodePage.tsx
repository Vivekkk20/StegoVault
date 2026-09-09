import React from 'react';
import { EncodeForm } from '../components/encode/EncodeForm';

export const EncodePage: React.FC = () => {
  return (
    <div className="space-y-6 pb-12">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white tracking-wide">
          Steganographic Encoding & Cryptographic Hiding
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Encrypt your secret payload using authenticated AES-256-GCM and embed it losslessly into the cover image bit planes.
        </p>
      </div>

      <EncodeForm />
    </div>
  );
};
