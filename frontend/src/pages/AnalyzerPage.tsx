import { useState } from 'react';
import {
  ScanEye,
  RefreshCw,
  AlertCircle,
  FileDown,
  Printer,
  Shield,
  FileImage,
} from 'lucide-react';
import { FileUpload } from '../components/common/FileUpload';
import { RiskMeter } from '../components/common/RiskMeter';
import { HashDisplay } from '../components/common/HashDisplay';
import { EduCard } from '../components/common/EduCard';
import { EntropyCard } from '../components/analyzer/EntropyCard';
import { HistogramChart } from '../components/analyzer/HistogramChart';
import { LsbAnalysisCard } from '../components/analyzer/LsbAnalysisCard';
import { LsbVisualizer } from '../components/analyzer/LsbVisualizer';
import { CorrelationMatrix } from '../components/analyzer/CorrelationMatrix';
import { MetadataTable } from '../components/analyzer/MetadataTable';
import { TrailingDataCard } from '../components/analyzer/TrailingDataCard';
import { FindingsList } from '../components/analyzer/FindingsList';
import { api } from '../services/api';
import type { ForensicReport, DetectedIndicator } from '../types';

export const AnalyzerPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [report, setReport] = useState<ForensicReport | null>(null);

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select an image file to analyze.');
      return;
    }

    setError(null);
    setLoading(true);
    try {
      const data = await api.analyzeImage(file);
      setReport(data);
    } catch (err: any) {
      setError(err.message || 'Forensic analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setFile(null);
    setReport(null);
    setError(null);
  };

  return (
    <div className="space-y-6 pb-12">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white tracking-wide">
          StegoVault Forensic Steganalysis Engine
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Perform multi-layered statistical and structural audits on untrusted images without requiring a StegoVault container.
        </p>
      </div>

      <EduCard
        title="Forensic Steganalysis & Statistical Detection"
        category="Steganalysis Theory"
        takeaway="Steganalysis seeks statistical or structural anomalies created by bit modification. Absence of detected indicators does not prove an image is clean: low-rate steganography can blend into sensor noise."
      >
        <p>
          Lossless LSB steganography leaves statistical fingerprints: it equalizes adjacent pixel intensities (measured via <strong>Chi-Square PoV attacks</strong>), raises LSB bit-plane entropy towards 1.0 bit/symbol, balances 0/1 bit distribution tightly around 50.00%, and can disrupt inter-channel correlation. StegoVault audits all these dimensions simultaneously to compute a calibrated forensic risk score.
        </p>
      </EduCard>

      {!report ? (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur space-y-6 max-w-4xl mx-auto">
          <FileUpload
            onFileSelect={setFile}
            selectedFile={file}
            label="Upload Suspicious Image for Inspection"
            helperText="Lossless PNG or BMP files (Max 20MB)"
          />

          {error && (
            <div className="flex items-center gap-2 rounded-xl border border-rose-500/30 bg-rose-950/30 p-3.5 text-sm text-rose-300">
              <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" />
              <span>{error}</span>
            </div>
          )}

          <div className="flex justify-end">
            <button
              onClick={handleAnalyze}
              disabled={loading || !file}
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-600 to-emerald-600 px-6 py-3 text-sm font-bold text-slate-950 transition-all duration-200 hover:from-cyan-500 hover:to-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg glow-cyan"
            >
              {loading ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  <span>Computing Statistical Indicators...</span>
                </>
              ) : (
                <>
                  <ScanEye className="h-4 w-4 text-slate-950" />
                  <span>Analyze File & Generate Report</span>
                </>
              )}
            </button>
          </div>
        </div>
      ) : (
        /* Full Forensic Dashboard */
        <div className="space-y-6">
          {/* Header Controls & Export */}
          <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/90 p-4 backdrop-blur">
            <div>
              <span className="text-[10px] font-mono uppercase text-slate-500">Analysis Reference ID</span>
              <p className="font-mono text-xs font-bold text-cyan-400">{report.analysis_id}</p>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <a
                href={api.getExportUrl(report.analysis_id, 'html')}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-950 px-3 py-1.5 text-xs font-semibold text-slate-200 hover:bg-slate-800 hover:text-cyan-400 transition-colors"
              >
                <Printer className="h-3.5 w-3.5" />
                <span>Print / View HTML</span>
              </a>

              <a
                href={api.getExportUrl(report.analysis_id, 'json')}
                download={`stegovault_report_${report.analysis_id.slice(0, 8)}.json`}
                className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-950 px-3 py-1.5 text-xs font-semibold text-slate-200 hover:bg-slate-800 hover:text-cyan-400 transition-colors"
              >
                <FileDown className="h-3.5 w-3.5" />
                <span>Export JSON</span>
              </a>

              <button
                onClick={resetAnalysis}
                className="rounded-lg bg-cyan-500 hover:bg-cyan-400 px-3 py-1.5 text-xs font-bold text-slate-950 transition-colors ml-2"
              >
                Scan Another Image
              </button>
            </div>
          </div>

          {/* Top Section: File Info & Risk Score */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* File Info */}
            <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur lg:col-span-1 space-y-4">
              <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
                <FileImage className="h-4 w-4 text-cyan-400" />
                <h3 className="text-sm font-bold uppercase tracking-wider text-slate-200">
                  File Information
                </h3>
              </div>

              <div className="space-y-2.5 font-mono text-xs">
                <div className="flex justify-between py-1 border-b border-slate-800/60">
                  <span className="text-slate-500">Filename</span>
                  <span className="text-slate-200 truncate max-w-[160px] font-bold">
                    {report.section_1_file_information.filename}
                  </span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-800/60">
                  <span className="text-slate-500">Format</span>
                  <span className="text-cyan-400 font-bold">
                    {report.section_1_file_information.format}
                  </span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-800/60">
                  <span className="text-slate-500">File Size</span>
                  <span className="text-slate-200">
                    {report.section_1_file_information.file_size_kb} KB ({report.section_1_file_information.file_size_bytes.toLocaleString()} bytes)
                  </span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-800/60">
                  <span className="text-slate-500">Dimensions</span>
                  <span className="text-slate-200">
                    {report.section_1_file_information.dimensions.width} x {report.section_1_file_information.dimensions.height} px
                  </span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-slate-500">Color Mode</span>
                  <span className="text-slate-200">
                    {report.section_1_file_information.color_mode} ({report.section_1_file_information.channel_count} channels)
                  </span>
                </div>
              </div>
            </div>

            {/* Risk Assessment */}
            <div className="lg:col-span-2 space-y-4">
              <RiskMeter
                score={report.section_10_risk_score.score}
                riskLevel={report.section_10_risk_score.risk_level}
              />

              {/* Contributing Indicators Pills */}
              <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-4 backdrop-blur">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-2">
                  Contributing Forensic Indicators ({report.section_9_detected_indicators.length})
                </span>
                <div className="space-y-1.5">
                  {report.section_9_detected_indicators.map((ind: DetectedIndicator, i: number) => (
                    <div
                      key={i}
                      className="flex items-center justify-between py-1 px-2.5 rounded bg-slate-950/80 text-xs border border-slate-800/80"
                    >
                      <div className="flex items-center gap-2">
                        <span className={`font-mono font-bold ${ind.is_positive ? 'text-rose-400' : 'text-emerald-400'}`}>
                          {ind.impact}
                        </span>
                        <span className="font-semibold text-slate-200">{ind.name}</span>
                        <span className="text-[10px] text-slate-500 font-mono">({ind.evidence})</span>
                      </div>
                      <span className="text-[10px] uppercase font-mono text-slate-500">{ind.category}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Cryptographic Hashes */}
          <HashDisplay
            label="Cryptographic Hashes"
            sha256={report.section_2_cryptographic_hashes.sha256}
            sha512={report.section_2_cryptographic_hashes.sha512}
          />

          {/* Trailing Appended Data Alert */}
          <TrailingDataCard trailing={report.section_8_structural_analysis.trailing_data} />

          {/* Statistical Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <EntropyCard entropy={report.section_4_entropy_analysis} />
            <HistogramChart histogram={report.section_6_histogram_analysis} />
          </div>

          {/* LSB Analysis and Visual Microscope */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <LsbAnalysisCard lsb={report.section_5_lsb_analysis} />
            <LsbVisualizer visualLsbPlane={report.section_5_lsb_analysis.visual_lsb_plane} />
          </div>

          {/* Channel Correlation and Metadata */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <CorrelationMatrix correlation={report.section_7_channel_correlation} />
            <MetadataTable metadata={report.section_3_metadata_analysis} />
          </div>

          {/* Technical Findings */}
          <FindingsList findings={report.section_11_technical_findings} />

          {/* Final Assessment & Legal Limitations */}
          <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-6 backdrop-blur space-y-4">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-200 flex items-center gap-2">
                <Shield className="h-4 w-4 text-cyan-400" />
                <span>Final Forensic Assessment</span>
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-300">
                {report.section_12_final_assessment}
              </p>
            </div>

            <div className="rounded-lg bg-rose-950/20 border border-rose-500/30 p-4 text-xs text-rose-200/90 leading-relaxed">
              <span className="font-bold uppercase tracking-wider block mb-1 text-rose-300">
                Forensic Limitation Notice:
              </span>
              {report.section_13_limitations}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
