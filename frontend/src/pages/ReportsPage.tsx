import { useState, useEffect } from 'react';
import {
  FileText,
  Trash2,
  ExternalLink,
  Download,
  Search,
  RefreshCw,
  ArrowLeft,
} from 'lucide-react';
import { api } from '../services/api';
import type { ReportSummary, ForensicReport } from '../types';
import { RiskMeter } from '../components/common/RiskMeter';
import { HashDisplay } from '../components/common/HashDisplay';
import { EntropyCard } from '../components/analyzer/EntropyCard';
import { HistogramChart } from '../components/analyzer/HistogramChart';
import { LsbAnalysisCard } from '../components/analyzer/LsbAnalysisCard';
import { LsbVisualizer } from '../components/analyzer/LsbVisualizer';
import { FindingsList } from '../components/analyzer/FindingsList';

interface ReportsPageProps {
  initialReportId?: string;
}

export const ReportsPage: React.FC<ReportsPageProps> = ({ initialReportId }) => {
  const [reports, setReports] = useState<ReportSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedReport, setSelectedReport] = useState<ForensicReport | null>(null);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const data = await api.listReports();
      setReports(data);
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  useEffect(() => {
    if (initialReportId) {
      loadReport(initialReportId);
    }
  }, [initialReportId]);

  const loadReport = async (id: string) => {
    try {
      const rep = await api.getReport(id);
      setSelectedReport(rep);
    } catch (err: any) {
      alert(err.message || 'Failed to load report.');
    }
  };

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this forensic report?')) return;
    try {
      await api.deleteReport(id);
      if (selectedReport?.analysis_id === id) {
        setSelectedReport(null);
      }
      fetchReports();
    } catch (err: any) {
      alert(err.message || 'Failed to delete report.');
    }
  };

  const filteredReports = reports.filter((r: ReportSummary) =>
    r.filename.toLowerCase().includes(search.toLowerCase()) ||
    r.risk_level.toLowerCase().includes(search.toLowerCase()) ||
    r.analysis_id.toLowerCase().includes(search.toLowerCase())
  );

  const getRiskBadge = (score: number, level: string) => {
    let color = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    if (score > 60) color = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
    else if (score > 40) color = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    else if (score > 20) color = 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30';

    return (
      <span className={`inline-flex items-center rounded border px-2 py-0.5 text-[10px] font-bold uppercase font-mono ${color}`}>
        {score} / 100 • {level.replace('_', ' ')}
      </span>
    );
  };

  return (
    <div className="space-y-6 pb-12">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white tracking-wide">
          Forensic Report Repository & Archive
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Historical records of computed forensic analyses with exportable HTML documents and raw JSON telemetry.
        </p>
      </div>

      {selectedReport ? (
        /* Detailed Report View */
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setSelectedReport(null)}
              className="flex items-center gap-1.5 text-xs text-cyan-400 hover:text-cyan-300 font-semibold"
            >
              <ArrowLeft className="h-4 w-4" /> Back to All Reports
            </button>

            <div className="flex items-center gap-2">
              <a
                href={api.getExportUrl(selectedReport.analysis_id, 'html')}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-950 px-3 py-1.5 text-xs font-semibold text-slate-200 hover:text-cyan-400 transition-colors"
              >
                <ExternalLink className="h-3.5 w-3.5" />
                <span>View Full HTML Report</span>
              </a>
              <a
                href={api.getExportUrl(selectedReport.analysis_id, 'json')}
                download={`report_${selectedReport.analysis_id.slice(0, 8)}.json`}
                className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-950 px-3 py-1.5 text-xs font-semibold text-slate-200 hover:text-cyan-400 transition-colors"
              >
                <Download className="h-3.5 w-3.5" />
                <span>Download JSON</span>
              </a>
            </div>
          </div>

          <RiskMeter
            score={selectedReport.section_10_risk_score.score}
            riskLevel={selectedReport.section_10_risk_score.risk_level}
          />

          <HashDisplay
            label="Cryptographic Hashes"
            sha256={selectedReport.section_2_cryptographic_hashes.sha256}
            sha512={selectedReport.section_2_cryptographic_hashes.sha512}
          />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <EntropyCard entropy={selectedReport.section_4_entropy_analysis} />
            <HistogramChart histogram={selectedReport.section_6_histogram_analysis} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <LsbAnalysisCard lsb={selectedReport.section_5_lsb_analysis} />
            <LsbVisualizer visualLsbPlane={selectedReport.section_5_lsb_analysis.visual_lsb_plane} />
          </div>

          <FindingsList findings={selectedReport.section_11_technical_findings} />
        </div>
      ) : (
        /* Report History List */
        <div className="space-y-4">
          <div className="flex items-center justify-between gap-4">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search by filename, risk level, or report ID..."
                className="w-full rounded-xl border border-slate-800 bg-slate-950 pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
              />
            </div>

            <button
              onClick={fetchReports}
              className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-cyan-400 transition-colors"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Refresh</span>
            </button>
          </div>

          {loading ? (
            <div className="p-12 text-center text-xs text-slate-500 flex items-center justify-center gap-2">
              <RefreshCw className="h-4 w-4 animate-spin text-cyan-400" />
              <span>Loading saved reports...</span>
            </div>
          ) : filteredReports.length === 0 ? (
            <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-12 text-center text-xs text-slate-500">
              <FileText className="h-8 w-8 mx-auto mb-2 text-slate-600" />
              <p>No forensic analysis reports found.</p>
              <p className="mt-1 text-slate-600">
                Run an image through the Forensic Analyzer to generate reports.
              </p>
            </div>
          ) : (
            <div className="divide-y divide-slate-800/80 rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur overflow-hidden">
              {filteredReports.map((rep: ReportSummary) => (
                <div
                  key={rep.analysis_id}
                  onClick={() => loadReport(rep.analysis_id)}
                  className="flex items-center justify-between p-4 cursor-pointer hover:bg-slate-800/40 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="rounded-xl bg-slate-950 p-2.5 text-cyan-400 border border-slate-800">
                      <FileText className="h-5 w-5" />
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-slate-200">{rep.filename}</h4>
                      <p className="font-mono text-xs text-slate-500 mt-0.5">
                        ID: {rep.analysis_id.slice(0, 13)}... • {new Date(rep.timestamp).toLocaleString()} • {rep.file_size_kb} KB ({rep.format})
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    {getRiskBadge(rep.risk_score, rep.risk_level)}
                    <button
                      onClick={(e) => handleDelete(e, rep.analysis_id)}
                      className="text-slate-500 hover:text-rose-400 p-1 transition-colors"
                      title="Delete report"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
