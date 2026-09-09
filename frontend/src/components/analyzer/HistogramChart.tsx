import React, { useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { BarChart3, AlertCircle } from 'lucide-react';
import type { HistogramAnalysis } from '../../types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface HistogramChartProps {
  histogram: HistogramAnalysis;
}

export const HistogramChart: React.FC<HistogramChartProps> = ({ histogram }) => {
  const [activeChannel, setActiveChannel] = useState<'all' | 'red' | 'green' | 'blue' | 'luminance'>('all');

  // Generate labels 0..255 (sampled every 4 bins for UI smoothness if desired, or all 256)
  const labels = Array.from({ length: 256 }, (_, i) => i.toString());

  const datasets = [];

  if (activeChannel === 'all' || activeChannel === 'red') {
    datasets.push({
      label: 'Red Channel',
      data: histogram.histograms.red,
      borderColor: 'rgba(239, 68, 68, 0.85)',
      backgroundColor: 'rgba(239, 68, 68, 0.1)',
      borderWidth: 1.5,
      pointRadius: 0,
      tension: 0.1,
    });
  }

  if (activeChannel === 'all' || activeChannel === 'green') {
    datasets.push({
      label: 'Green Channel',
      data: histogram.histograms.green,
      borderColor: 'rgba(34, 197, 94, 0.85)',
      backgroundColor: 'rgba(34, 197, 94, 0.1)',
      borderWidth: 1.5,
      pointRadius: 0,
      tension: 0.1,
    });
  }

  if (activeChannel === 'all' || activeChannel === 'blue') {
    datasets.push({
      label: 'Blue Channel',
      data: histogram.histograms.blue,
      borderColor: 'rgba(59, 130, 246, 0.85)',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      borderWidth: 1.5,
      pointRadius: 0,
      tension: 0.1,
    });
  }

  if (activeChannel === 'luminance') {
    datasets.push({
      label: 'Luminance',
      data: histogram.histograms.luminance,
      borderColor: 'rgba(245, 158, 11, 0.85)',
      backgroundColor: 'rgba(245, 158, 11, 0.1)',
      borderWidth: 1.5,
      pointRadius: 0,
      tension: 0.1,
    });
  }

  const data = {
    labels,
    datasets,
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index' as const,
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: '#94a3b8',
          font: { size: 11 },
        },
      },
      tooltip: {
        backgroundColor: '#0f172a',
        borderColor: '#334155',
        borderWidth: 1,
        titleColor: '#e2e8f0',
        bodyColor: '#94a3b8',
      },
    },
    scales: {
      x: {
        grid: { color: '#1e293b' },
        ticks: { color: '#64748b', maxTicksLimit: 16, font: { size: 10 } },
        title: { display: true, text: 'Pixel Intensity (0 - 255)', color: '#64748b', font: { size: 10 } },
      },
      y: {
        grid: { color: '#1e293b' },
        ticks: { color: '#64748b', font: { size: 10 } },
        title: { display: true, text: 'Frequency Count', color: '#64748b', font: { size: 10 } },
      },
    },
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <BarChart3 className="h-4 w-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            RGB Channel Histograms (256 Bins)
          </h3>
        </div>

        {/* Filter controls */}
        <div className="flex items-center gap-1 text-xs">
          {(['all', 'red', 'green', 'blue', 'luminance'] as const).map((ch) => (
            <button
              key={ch}
              onClick={() => setActiveChannel(ch)}
              className={`px-2.5 py-1 rounded capitalize font-medium transition-colors ${
                activeChannel === ch
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`}
            >
              {ch}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-4 h-64 w-full">
        <Line data={data} options={options} />
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2 border-t border-slate-800/80 pt-3">
        <div className="text-center bg-slate-950 p-2 rounded">
          <span className="text-[10px] text-slate-500 uppercase">Red PoV Delta</span>
          <p className="font-mono text-xs text-slate-200">
            {histogram.pov_pairing_delta.red?.toFixed(4) ?? 'N/A'}
          </p>
        </div>
        <div className="text-center bg-slate-950 p-2 rounded">
          <span className="text-[10px] text-slate-500 uppercase">Green PoV Delta</span>
          <p className="font-mono text-xs text-slate-200">
            {histogram.pov_pairing_delta.green?.toFixed(4) ?? 'N/A'}
          </p>
        </div>
        <div className="text-center bg-slate-950 p-2 rounded">
          <span className="text-[10px] text-slate-500 uppercase">Blue PoV Delta</span>
          <p className="font-mono text-xs text-slate-200">
            {histogram.pov_pairing_delta.blue?.toFixed(4) ?? 'N/A'}
          </p>
        </div>
      </div>

      {histogram.is_flattened_anomaly && (
        <div className="mt-3 flex items-center gap-2 rounded bg-amber-500/10 p-2 text-xs text-amber-300 border border-amber-500/30">
          <AlertCircle className="h-4 w-4 shrink-0 text-amber-400" />
          <span>{histogram.evaluation}</span>
        </div>
      )}
    </div>
  );
};
