import { MetricCard } from "@/components/metric-card";
import { QualityScoreBadge } from "@/components/quality-score-badge";
import { DataQualityBanner } from "@/components/data-quality-banner";
import { ColumnSchemaTable } from "@/components/column-schema-table";
import type { DatasetUploadResponse } from "@/lib/types";

function formatCount(n: number): string {
  return new Intl.NumberFormat("en-US").format(n);
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export function DatasetProfileDashboard({ dataset, profile }: DatasetUploadResponse) {
  return (
    <div className="w-full space-y-6">
      <div>
        <h2 className="text-lg font-semibold">{dataset.filename}</h2>
        <p className="text-sm text-muted">
          Uploaded {new Date(dataset.uploaded_at).toLocaleString()} · {dataset.file_type.toUpperCase()}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <MetricCard label="Total Rows" value={formatCount(profile.row_count)} />
        <MetricCard label="Columns" value={formatCount(profile.column_count)} />
        <MetricCard label="File Size" value={formatFileSize(dataset.file_size_bytes)} />
        <QualityScoreBadge score={profile.quality_score} />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <MetricCard
          label="Duplicate Rows"
          value={formatCount(profile.duplicate_row_count)}
          hint={
            profile.row_count > 0
              ? `${((profile.duplicate_row_count / profile.row_count) * 100).toFixed(1)}% of rows`
              : undefined
          }
        />
      </div>

      <DataQualityBanner issues={profile.issues} />

      <div>
        <h3 className="mb-3 text-sm font-medium uppercase tracking-wide text-muted">
          Column Schema
        </h3>
        <ColumnSchemaTable columns={profile.columns} />
      </div>
    </div>
  );
}
