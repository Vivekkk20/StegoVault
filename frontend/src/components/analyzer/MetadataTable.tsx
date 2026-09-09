import { Tag, AlertTriangle } from 'lucide-react';

interface MetadataTableProps {
  metadata: {
    has_exif: boolean;
    exif_count: number;
    exif_fields: Record<string, string>;
    png_text_chunks: Array<{ type: string; length: number; preview: string }>;
    suspicious_tags: Array<{ tag: string; preview: string; length: number }>;
  };
}

export const MetadataTable: React.FC<MetadataTableProps> = ({ metadata }) => {
  const hasMetadata =
    metadata.has_exif ||
    metadata.png_text_chunks.length > 0 ||
    metadata.suspicious_tags.length > 0;

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Tag className="h-4 w-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            Metadata & Header Chunks Inspection
          </h3>
        </div>
        {metadata.suspicious_tags.length > 0 && (
          <span className="flex items-center gap-1 rounded bg-amber-500/10 px-2 py-0.5 text-xs font-semibold text-amber-400 border border-amber-500/30">
            <AlertTriangle className="h-3 w-3" /> Suspicious Tags Found
          </span>
        )}
      </div>

      {!hasMetadata ? (
        <div className="mt-4 p-4 text-center text-xs text-slate-500 bg-slate-950 rounded border border-slate-800/80">
          No EXIF or extended text metadata chunks present in this image header.
        </div>
      ) : (
        <div className="mt-4 space-y-4">
          {/* Suspicious tags banner */}
          {metadata.suspicious_tags.length > 0 && (
            <div className="rounded-lg bg-amber-950/20 border border-amber-500/30 p-3 text-xs text-amber-200">
              <span className="font-bold">Flagged Metadata: </span>
              {metadata.suspicious_tags.map((t, idx) => (
                <div key={idx} className="mt-1 font-mono">
                  • <strong>{t.tag}</strong> ({t.length} chars): {t.preview}
                </div>
              ))}
            </div>
          )}

          {/* PNG text chunks */}
          {metadata.png_text_chunks.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold uppercase text-slate-400 mb-2">
                PNG Text Chunks (tEXt / zTXt / iTXt)
              </h4>
              <div className="space-y-1.5 font-mono text-xs">
                {metadata.png_text_chunks.map((chunk, i) => (
                  <div key={i} className="flex justify-between items-center bg-slate-950 p-2 rounded border border-slate-800">
                    <span className="text-cyan-400 font-bold">{chunk.type} ({chunk.length} bytes)</span>
                    <span className="text-slate-300 truncate max-w-xs">{chunk.preview}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* EXIF Fields */}
          {metadata.has_exif && (
            <div>
              <h4 className="text-xs font-semibold uppercase text-slate-400 mb-2">
                EXIF Attributes ({metadata.exif_count} tags)
              </h4>
              <div className="max-h-48 overflow-y-auto space-y-1 font-mono text-xs">
                {Object.entries(metadata.exif_fields).map(([key, val]) => (
                  <div key={key} className="flex justify-between py-1 px-2 bg-slate-950/60 rounded border border-slate-800/60">
                    <span className="text-slate-400">{key}</span>
                    <span className="text-slate-200 truncate max-w-sm">{val}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
