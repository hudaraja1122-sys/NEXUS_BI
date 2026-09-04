import { AlertTriangle } from "lucide-react";
import type { DataQualityIssue, IssueSeverity } from "@/lib/types";

const SEVERITY_ORDER: IssueSeverity[] = ["high", "medium", "low"];

const SEVERITY_STYLES: Record<IssueSeverity, string> = {
  high: "border-red-500/30 bg-red-500/5 text-red-500",
  medium: "border-amber-500/30 bg-amber-500/5 text-amber-500",
  low: "border-muted/30 bg-muted/5 text-muted",
};

export function DataQualityBanner({ issues }: { issues: DataQualityIssue[] }) {
  if (issues.length === 0) {
    return (
      <div className="rounded-panel border border-mint/30 bg-mint/5 px-5 py-4 text-sm text-mint">
        No data quality issues detected.
      </div>
    );
  }

  const sorted = [...issues].sort(
    (a, b) => SEVERITY_ORDER.indexOf(a.severity) - SEVERITY_ORDER.indexOf(b.severity),
  );

  return (
    <div className="rounded-panel border border-border p-5">
      <div className="mb-3 flex items-center gap-2">
        <AlertTriangle className="h-4 w-4 text-amber-500" />
        <p className="font-medium">
          {issues.length} data quality {issues.length === 1 ? "issue" : "issues"} found
        </p>
      </div>
      <ul className="space-y-2">
        {sorted.map((issue, i) => (
          <li
            key={`${issue.column}-${issue.issue_type}-${i}`}
            className={`rounded-lg border px-3 py-2 text-sm ${SEVERITY_STYLES[issue.severity]}`}
          >
            <span className="font-medium">
              {issue.column === "*" ? "Dataset" : issue.column}
            </span>{" "}
            — {issue.detail}
          </li>
        ))}
      </ul>
    </div>
  );
}
