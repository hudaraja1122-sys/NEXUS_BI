"use client";

import { useMemo, useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import type { ColumnProfile, ColumnType } from "@/lib/types";

type SortKey = "name" | "null_pct" | "unique_count";

const TYPE_STYLES: Record<ColumnType, string> = {
  numeric: "bg-blue-500/10 text-blue-500",
  categorical: "bg-purple-500/10 text-purple-500",
  datetime: "bg-mint/10 text-mint",
  boolean: "bg-amber-500/10 text-amber-500",
  text: "bg-muted/10 text-muted",
};

function SortHeader({
  label,
  active,
  direction,
  onClick,
}: {
  label: string;
  active: boolean;
  direction: "asc" | "desc";
  onClick: () => void;
}) {
  return (
    <th
      onClick={onClick}
      className="cursor-pointer select-none px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-muted hover:text-foreground"
    >
      <span className="inline-flex items-center gap-1">
        {label}
        {active &&
          (direction === "asc" ? (
            <ChevronUp className="h-3 w-3" />
          ) : (
            <ChevronDown className="h-3 w-3" />
          ))}
      </span>
    </th>
  );
}

export function ColumnSchemaTable({ columns }: { columns: ColumnProfile[] }) {
  const [sortKey, setSortKey] = useState<SortKey>("name");
  const [direction, setDirection] = useState<"asc" | "desc">("asc");

  const toggleSort = (key: SortKey) => {
    if (sortKey === key) {
      setDirection((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setDirection("asc");
    }
  };

  const sorted = useMemo(() => {
    const copy = [...columns];
    copy.sort((a, b) => {
      let cmp = 0;
      if (sortKey === "name") cmp = a.name.localeCompare(b.name);
      if (sortKey === "null_pct") cmp = a.null_pct - b.null_pct;
      if (sortKey === "unique_count") cmp = a.unique_count - b.unique_count;
      return direction === "asc" ? cmp : -cmp;
    });
    return copy;
  }, [columns, sortKey, direction]);

  return (
    <div className="overflow-hidden rounded-panel border border-border">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[640px] border-collapse text-sm">
          <thead className="border-b border-border">
            <tr>
              <SortHeader
                label="Column"
                active={sortKey === "name"}
                direction={direction}
                onClick={() => toggleSort("name")}
              />
              <th className="px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-muted">
                Type
              </th>
              <SortHeader
                label="Nulls"
                active={sortKey === "null_pct"}
                direction={direction}
                onClick={() => toggleSort("null_pct")}
              />
              <SortHeader
                label="Unique"
                active={sortKey === "unique_count"}
                direction={direction}
                onClick={() => toggleSort("unique_count")}
              />
              <th className="px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-muted">
                Sample values
              </th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((col) => (
              <tr key={col.name} className="border-b border-border last:border-0">
                <td className="px-4 py-3 font-medium">{col.name}</td>
                <td className="px-4 py-3">
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-medium ${TYPE_STYLES[col.inferred_type]}`}
                  >
                    {col.inferred_type}
                  </span>
                </td>
                <td className="px-4 py-3 text-muted">
                  {col.null_count} <span className="text-xs">({col.null_pct}%)</span>
                </td>
                <td className="px-4 py-3 text-muted">{col.unique_count}</td>
                <td className="max-w-[280px] truncate px-4 py-3 text-xs text-muted">
                  {col.sample_values.map(String).join(", ")}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
