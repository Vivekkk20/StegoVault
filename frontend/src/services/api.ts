import type {
  CapacityData,
  EncodeResponse,
  DecodeResponse,
  DetectionResponse,
  ForensicReport,
  ReportSummary,
} from '../types';

const API_BASE = '/api/v1';

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorMsg = `Server returned status ${res.status}`;
    try {
      const json = await res.json();
      errorMsg = json.detail || json.message || errorMsg;
    } catch {
      // ignore
    }
    throw new Error(errorMsg);
  }
  return res.json();
}

export const api = {
  async getHealth() {
    const res = await fetch(`${API_BASE}/health`);
    return handleResponse<{ status: string; app_name: string; security: any }>(res);
  },

  async checkCapacity(file: File, message: string = ''): Promise<CapacityData> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('message', message);
    const res = await fetch(`${API_BASE}/steganography/capacity`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<CapacityData>(res);
  },

  async detectPayload(file: File): Promise<DetectionResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/steganography/detect`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<DetectionResponse>(res);
  },

  async encodeMessage(formData: FormData): Promise<EncodeResponse> {
    const res = await fetch(`${API_BASE}/steganography/encode`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<EncodeResponse>(res);
  },

  async decodeMessage(file: File, password: string): Promise<DecodeResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('password', password);
    const res = await fetch(`${API_BASE}/steganography/decode`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<DecodeResponse>(res);
  },

  async analyzeImage(file: File): Promise<ForensicReport> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/analyzer/analyze`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<ForensicReport>(res);
  },

  async getReport(analysisId: string): Promise<ForensicReport> {
    const res = await fetch(`${API_BASE}/reports/${analysisId}`);
    return handleResponse<ForensicReport>(res);
  },

  async listReports(): Promise<ReportSummary[]> {
    const res = await fetch(`${API_BASE}/reports`);
    return handleResponse<ReportSummary[]>(res);
  },

  async deleteReport(reportId: string): Promise<{ success: boolean }> {
    const res = await fetch(`${API_BASE}/reports/${reportId}`, {
      method: 'DELETE',
    });
    return handleResponse<{ success: boolean }>(res);
  },

  getExportUrl(reportId: string, format: 'html' | 'json' = 'html') {
    return `${API_BASE}/reports/${reportId}/export?format=${format}`;
  },
};
