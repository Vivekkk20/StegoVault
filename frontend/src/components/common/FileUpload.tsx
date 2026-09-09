import { useState, useRef } from 'react';
import { UploadCloud, X, AlertCircle } from 'lucide-react';

interface FileUploadProps {
  onFileSelect: (file: File | null) => void;
  selectedFile: File | null;
  label?: string;
  acceptFormats?: string;
  helperText?: string;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  selectedFile,
  label = 'Select Cover Image',
  acceptFormats = '.png,.bmp',
  helperText = 'Lossless PNG or BMP files only (Max 20MB)',
}) => {
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File | null) => {
    setError(null);
    if (!file) {
      setPreviewUrl(null);
      onFileSelect(null);
      return;
    }

    const name = file.name.toLowerCase();
    if (!name.endsWith('.png') && !name.endsWith('.bmp')) {
      setError('Invalid format: Only lossless PNG and BMP images are supported.');
      return;
    }

    if (file.size > 20 * 1024 * 1024) {
      setError('File is too large: Maximum upload size is 20MB.');
      return;
    }

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    onFileSelect(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const clearFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (inputRef.current) inputRef.current.value = '';
    handleFile(null);
  };

  return (
    <div className="w-full">
      <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
        {label}
      </label>

      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        className={`group relative flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-6 text-center transition-all duration-200 ${
          dragOver
            ? 'border-cyan-400 bg-cyan-950/30'
            : selectedFile
            ? 'border-slate-700 bg-slate-900/80 hover:border-cyan-500/50'
            : 'border-slate-800 bg-slate-950/60 hover:border-slate-700 hover:bg-slate-900/40'
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept={acceptFormats}
          className="hidden"
          onChange={(e) => e.target.files && handleFile(e.target.files[0])}
        />

        {selectedFile && previewUrl ? (
          <div className="flex w-full items-center justify-between gap-4">
            <div className="flex items-center gap-4 overflow-hidden">
              <div className="h-16 w-16 shrink-0 overflow-hidden rounded-lg border border-slate-700 bg-slate-950">
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="h-full w-full object-cover"
                />
              </div>
              <div className="text-left overflow-hidden">
                <p className="truncate text-sm font-semibold text-slate-200">
                  {selectedFile.name}
                </p>
                <p className="text-xs text-slate-400 font-mono">
                  {(selectedFile.size / 1024).toFixed(1)} KB • {selectedFile.type || 'image'}
                </p>
                <span className="inline-block mt-1 text-[10px] font-semibold uppercase tracking-wider text-emerald-400">
                  ✓ Verified Lossless Image
                </span>
              </div>
            </div>

            <button
              onClick={clearFile}
              className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-rose-400 transition-colors"
              title="Remove file"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-2">
            <div className="rounded-full bg-slate-900 p-3 text-cyan-400 group-hover:scale-110 transition-transform">
              <UploadCloud className="h-6 w-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-200">
                Drop your image here, or <span className="text-cyan-400 underline">browse</span>
              </p>
              <p className="mt-1 text-xs text-slate-500">{helperText}</p>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-2 flex items-center gap-1.5 text-xs text-rose-400">
          <AlertCircle className="h-4 w-4" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};
