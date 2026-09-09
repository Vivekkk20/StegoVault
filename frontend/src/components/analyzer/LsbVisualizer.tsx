import React, { useState } from 'react';
import { Eye, ZoomIn, Info } from 'lucide-react';

interface LsbVisualizerProps {
  visualLsbPlane: string;
}

export const LsbVisualizer: React.FC<LsbVisualizerProps> = ({ visualLsbPlane }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Eye className="h-4 w-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            Visual LSB Bit-Plane Extraction
          </h3>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-1.5 rounded-lg border border-slate-800 bg-slate-950 px-2.5 py-1 text-xs text-slate-300 hover:text-cyan-400 hover:border-slate-700 transition-colors"
        >
          <ZoomIn className="h-3.5 w-3.5" />
          <span>Full Inspect</span>
        </button>
      </div>

      <div className="mt-4 flex flex-col md:flex-row gap-5 items-center">
        {/* Preview image */}
        <div
          onClick={() => setIsModalOpen(true)}
          className="group relative h-48 w-48 shrink-0 cursor-pointer overflow-hidden rounded-lg border border-slate-700 bg-slate-950"
        >
          <img
            src={visualLsbPlane}
            alt="Visual LSB Bit Plane"
            className="h-full w-full object-contain pixelated"
          />
          <div className="absolute inset-0 flex items-center justify-center bg-slate-950/60 opacity-0 group-hover:opacity-100 transition-opacity">
            <span className="flex items-center gap-1 text-xs font-semibold text-cyan-400">
              <ZoomIn className="h-4 w-4" /> Click to Zoom
            </span>
          </div>
        </div>

        {/* Visual forensic explanation */}
        <div className="flex-1 space-y-3 text-xs text-slate-400">
          <div className="flex items-start gap-2 bg-slate-950 p-3 rounded-lg border border-slate-800/80">
            <Info className="h-4 w-4 shrink-0 text-cyan-400 mt-0.5" />
            <div>
              <span className="font-semibold text-slate-200">How to interpret: </span>
              <p className="mt-1 leading-relaxed">
                • <strong className="text-emerald-400">Natural image LSBs:</strong> You can faintly observe edges, shapes, and contours from the original scene.
              </p>
              <p className="mt-1 leading-relaxed">
                • <strong className="text-rose-400">Encrypted stego LSBs:</strong> Pixels overwritten with high-entropy ciphertext appear as completely random black-and-white static/snow without recognizable contours.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Modal View */}
      {isModalOpen && (
        <div
          onClick={() => setIsModalOpen(false)}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm"
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="relative max-h-[90vh] max-w-[90vw] overflow-auto rounded-2xl border border-slate-700 bg-slate-950 p-6 shadow-2xl"
          >
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-sm font-bold uppercase text-slate-200">
                LSB Bit-Plane Forensic Microscope (Scaled 0 or 255)
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="rounded-lg p-1 text-slate-400 hover:text-white"
              >
                ✕
              </button>
            </div>
            <img
              src={visualLsbPlane}
              alt="Zoomed LSB Bit Plane"
              className="max-h-[75vh] w-auto mx-auto rounded border border-slate-800 pixelated"
            />
          </div>
        </div>
      )}
    </div>
  );
};
