// Mirrors backend/app/models/schemas.py — keep these two in sync manually
// until Phase 4+ introduces generated types from the OpenAPI schema.

export type ColumnType = "numeric" | "categorical" | "datetime" | "boolean" | "text";
export type IssueSeverity = "low" | "medium" | "high";
export type IssueType =
  | "missing_values"
  | "duplicate_rows"
  | "constant_column"
  | "high_cardinality"
  | "mixed_types";

export interface ColumnProfile {
  name: string;
  inferred_type: ColumnType;
  null_count: number;
  null_pct: number;
  unique_count: number;
  sample_values: unknown[];
  min_value: number | null;
  max_value: number | null;
  mean_value: number | null;
  median_value: number | null;
  std_value: number | null;
}

export interface DataQualityIssue {
  column: string;
  issue_type: IssueType;
  severity: IssueSeverity;
  detail: string;
}

export interface DatasetProfile {
  row_count: number;
  column_count: number;
  duplicate_row_count: number;
  quality_score: number;
  columns: ColumnProfile[];
  issues: DataQualityIssue[];
}

export interface DatasetSummary {
  id: string;
  filename: string;
  file_type: "csv" | "xlsx";
  uploaded_at: string;
  file_size_bytes: number;
  row_count: number;
  column_count: number;
  quality_score: number;
}

export interface DatasetUploadResponse {
  dataset: DatasetSummary;
  profile: DatasetProfile;
}

export interface ApiErrorBody {
  detail: string;
}
