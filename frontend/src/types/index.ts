export interface CapacityData {
  width: number;
  height: number;
  total_pixels: number;
  channels_used: number;
  bits_per_channel: number;
  capacity_bits: number;
  capacity_bytes: number;
  capacity_kb: number;
  required_bytes?: number;
  required_kb?: number;
  sufficient_capacity?: boolean;
  utilization_percentage?: number;
  status?: string;
}

export interface EncodeResponse {
  success: boolean;
  message: string;
  output_filename: string;
  dimensions: string;
  mode: string;
  payload_bytes: number;
  capacity_bytes: number;
  capacity_utilization: number;
  cover_sha256: string;
  stego_sha256: string;
  download_url: string;
}

export interface DecodeResponse {
  success: boolean;
  secret_message: string;
  payload_bytes: number;
  ciphertext_bytes: number;
  version: number;
  compressed: boolean;
  integrity_verified: boolean;
  stego_sha256: string;
}

export interface DetectionResponse {
  detected: boolean;
  version?: number;
  flags?: number;
  iterations?: number;
  compressed?: boolean;
  ciphertext_length?: number;
  total_payload_bytes?: number;
  header_crc_valid?: boolean;
  reason?: string;
  error?: string;
}

export interface FileInfo {
  filename: string;
  format: string;
  file_size_bytes: number;
  file_size_kb: number;
  dimensions: {
    width: number;
    height: number;
    aspect_ratio: number;
    total_pixels: number;
  };
  color_mode: string;
  channel_count: number;
}

export interface Hashes {
  sha256: string;
  sha512: string;
}

export interface EntropyAnalysis {
  file_entropy: number;
  pixel_entropy: number;
  channels_entropy: Record<string, number>;
  lsb_bit_entropy: Record<string, number>;
  suspicious_channels: string[];
  is_lsb_anomaly: boolean;
  evaluation: string;
}

export interface LsbChannelData {
  distribution: {
    count_0: number;
    count_1: number;
    percentage_0: number;
    percentage_1: number;
    deviation_from_50: number;
    status: string;
  };
  chi_square?: {
    chi2_statistic: number;
    degrees_of_freedom: number;
    p_value: number;
    evaluated_pairs: number;
    is_suspicious: boolean;
    status: string;
  };
  status: string;
}

export interface LSBAnalysis {
  channels: Record<string, LsbChannelData>;
  suspicious_channels_count: number;
  summary: string;
  visual_lsb_plane: string;
}

export interface HistogramAnalysis {
  histograms: {
    red: number[];
    green: number[];
    blue: number[];
    luminance: number[];
  };
  pov_pairing_delta: Record<string, number>;
  is_flattened_anomaly: boolean;
  evaluation: string;
}

export interface ChannelCorrelation {
  channel_correlation: {
    r_vs_g: number;
    r_vs_b: number;
    g_vs_b: number;
  };
  lsb_plane_correlation: {
    r_vs_g: number;
    r_vs_b: number;
    g_vs_b: number;
  };
  is_correlation_anomaly: boolean;
  evaluation: string;
}

export interface TrailingDataInfo {
  detected: boolean;
  legal_eof_offset?: number;
  trailing_size_bytes: number;
  trailing_size_kb?: number;
  sha256?: string;
  preview_hex?: string;
  description?: string;
}

export interface StructuralAnalysis {
  trailing_data: TrailingDataInfo;
  chunks_summary: string[];
  anomalies: string[];
  stegovault_signature?: DetectionResponse;
}

export interface DetectedIndicator {
  name: string;
  impact: string;
  is_positive: boolean;
  category: string;
  evidence: string;
  explanation: string;
}

export interface RiskScore {
  score: number;
  risk_level: 'VERY_LOW' | 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
}

export interface TechnicalFinding {
  severity: 'INFO' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  category: string;
  title: string;
  description: string;
  evidence: string;
}

export interface ForensicReport {
  analysis_id: string;
  timestamp: string;
  section_1_file_information: FileInfo;
  section_2_cryptographic_hashes: Hashes;
  section_3_metadata_analysis: {
    has_exif: boolean;
    exif_count: number;
    exif_fields: Record<string, string>;
    png_text_chunks: Array<{ type: string; length: number; preview: string }>;
    suspicious_tags: Array<{ tag: string; preview: string; length: number }>;
  };
  section_4_entropy_analysis: EntropyAnalysis;
  section_5_lsb_analysis: LSBAnalysis;
  section_6_histogram_analysis: HistogramAnalysis;
  section_7_channel_correlation: ChannelCorrelation;
  section_8_structural_analysis: StructuralAnalysis;
  section_9_detected_indicators: DetectedIndicator[];
  section_10_risk_score: RiskScore;
  section_11_technical_findings: TechnicalFinding[];
  section_12_final_assessment: string;
  section_13_limitations: string;
}

export interface ReportSummary {
  analysis_id: string;
  timestamp: string;
  filename: string;
  format: string;
  file_size_kb: number;
  risk_score: number;
  risk_level: string;
}
