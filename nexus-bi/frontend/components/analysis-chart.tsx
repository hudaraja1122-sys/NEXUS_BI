"use client";

import React from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const CYAN_PALETTE = [
  "#00f0d2", // Primary Electric Cyan
  "#38bdf8", // Sky Blue
  "#818cf8", // Indigo Accent
  "#f43f5e", // Rose Pink (Losses)
  "#fbbf24", // Amber
  "#34d399", // Mint Green
];

export interface ChartSpecData {
  chart_type: string;
  title: string;
  x_axis?: string | null;
  y_axis?: string | null;
  series?: string | null;
}

interface AnalysisChartProps {
  chart: ChartSpecData;
  data: Record<string, any>[];
}

export function AnalysisChart({ chart, data }: AnalysisChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-2xl border border-white/10 bg-[#121624] p-6 text-center text-sm text-slate-400">
        No data returned for this query.
      </div>
    );
  }

  const sampleRow = data[0] || {};
  const dataKeys = Object.keys(sampleRow);

  function resolveKey(target: string | null | undefined, fallbackIndex: number): string {
    if (target) {
      if (target in sampleRow) return target;
      const matched = dataKeys.find(
        (k) => k.toLowerCase() === target.toLowerCase() || k.toLowerCase().replace(/_/g, "") === target.toLowerCase().replace(/_/g, "")
      );
      if (matched) return matched;
    }
    return dataKeys[fallbackIndex] || dataKeys[0] || "";
  }

  let xKey = resolveKey(chart.x_axis, 0);
  let yKey = resolveKey(chart.y_axis, 1);

  if (typeof sampleRow[xKey] === "number" && typeof sampleRow[yKey] === "string") {
    const temp = xKey;
    xKey = yKey;
    yKey = temp;
  }

  const formatValue = (val: any) => {
    if (typeof val === "number") return val.toLocaleString();
    return val;
  };

  return (
    <div className="w-full">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-base font-bold text-white">
          {chart.title || "Query Result"}
        </h3>
        <span className="rounded-full bg-[#202740] px-3 py-1 text-xs font-semibold text-[#00f0d2] border border-[#00f0d2]/20">
          {data.length} records
        </span>
      </div>

      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          {chart.chart_type === "line" ? (
            <LineChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262f4d" vertical={false} />
              <XAxis dataKey={xKey} stroke="#64748b" fontSize={12} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={formatValue} />
              <Tooltip 
                contentStyle={{ backgroundColor: "#1a2138", borderColor: "#00f0d2", borderRadius: 12, color: "#fff" }}
                formatter={(value: any) => [formatValue(value), yKey]} 
              />
              <Legend verticalAlign="top" height={36} wrapperStyle={{ color: "#fff" }} />
              <Line
                type="monotone"
                dataKey={yKey}
                stroke="#00f0d2"
                strokeWidth={3}
                dot={{ r: 5, fill: "#00f0d2" }}
              />
            </LineChart>
          ) : chart.chart_type === "pie" ? (
            <PieChart>
              <Tooltip contentStyle={{ backgroundColor: "#1a2138", borderColor: "#00f0d2", borderRadius: 12, color: "#fff" }} />
              <Legend verticalAlign="bottom" height={36} wrapperStyle={{ color: "#fff" }} />
              <Pie
                data={data}
                dataKey={yKey}
                nameKey={xKey}
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={({ name, percent }: any) => `${name} (${(percent * 100).toFixed(0)}%)`}
              >
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={CYAN_PALETTE[index % CYAN_PALETTE.length]} />
                ))}
              </Pie>
            </PieChart>
          ) : (
            <BarChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262f4d" vertical={false} />
              <XAxis dataKey={xKey} stroke="#64748b" fontSize={12} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={formatValue} />
              <Tooltip 
                contentStyle={{ backgroundColor: "#1a2138", borderColor: "#00f0d2", borderRadius: 12, color: "#fff" }}
                formatter={(value: any) => [formatValue(value), yKey]} 
              />
              <Legend verticalAlign="top" height={36} />
              <Bar dataKey={yKey} fill="#00f0d2" radius={[6, 6, 0, 0]} maxBarSize={55} />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
}