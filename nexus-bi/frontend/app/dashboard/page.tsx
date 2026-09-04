"use client";

import React, { useState } from "react";
import Link from "next/link";
import { UploadDropzone } from "@/components/upload-dropzone";
import { DatasetProfileDashboard } from "@/components/dataset-profile-dashboard";
import { AnalysisChart, ChartSpecData } from "@/components/analysis-chart";
import type { DatasetUploadResponse } from "@/lib/types";
import { 
  ArrowLeft, 
  Sparkles, 
  CheckCircle2, 
  GitCommit, 
  FileDown, 
  Loader2 
} from "lucide-react";

interface TraceStep {
  step: string;
  tool: string;
  action: string;
  status: string;
}

interface AnalysisResult {
  summary_text: string;
  findings?: Array<{ title: string; metric: string; detail: string }>;
  recommendations?: Array<{ priority: string; action: string; reason: string }>;
  chart: ChartSpecData;
  data: Record<string, any>[];
  kpis?: Record<string, any>;
  trace?: TraceStep[];
}

const SUGGESTED_QUESTIONS = [
  {
    label: "Root-Cause Profit Collapse (Recursive Loop)",
    query: "Why did profit collapse in Q2 and which products caused it?",
    icon: "🔬",
  },
  {
    label: "Quarterly Margin Decay (Line)",
    query: "Audit our quarterly margin trend and compare Q1 vs Q2.",
    icon: "📈",
  },
  {
    label: "Category Loss Distribution (Bar)",
    query: "Which product categories are running negative profit margins?",
    icon: "📊",
  },
  {
    label: "Discount Sensitivity Audit",
    query: "Are deep discounts above 30% destroying overall profitability?",
    icon: "🏷️",
  },
];

export default function DashboardPage() {
  const [result, setResult] = useState<DatasetUploadResponse | null>(null);
  const [prompt, setPrompt] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [exporting, setExporting] = useState<boolean>(false);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);

  async function executeAnalysis(queryText: string) {
    if (!queryText.trim() || !result?.dataset?.id) return;

    setLoading(true);
    setPrompt(queryText);

    try {
      const res = await fetch("/api/analysis/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          dataset_id: result.dataset.id,
          prompt: queryText.trim(),
        }),
      });

      if (!res.ok) {
        const errorData = await res
          .json()
          .catch(() => ({ detail: "Investigation failed." }));
        throw new Error(errorData.detail || "Investigation execution failed.");
      }

      const data: AnalysisResult = await res.json();
      setAnalysis(data);
    } catch (err: any) {
      alert(`Investigation failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function handleExportPDF() {
    if (!analysis || !result?.dataset?.filename) return;

    setExporting(true);
    try {
      const res = await fetch("/api/analysis/export-pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          dataset_name: result.dataset.filename,
          query_text: prompt,
          summary_text: analysis.summary_text,
          kpis: analysis.kpis || {},
          findings: analysis.findings || [],
          recommendations: analysis.recommendations || [],
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to generate executive report.");
      }

      const data = await res.json();
      window.open(data.download_url, "_blank");
    } catch (err: any) {
      alert(`Report export failed: ${err.message}`);
    } finally {
      setExporting(false);
    }
  }

  function handleFormSubmit(e: React.FormEvent) {
    e.preventDefault();
    executeAnalysis(prompt);
  }

  const dropzoneProps: any = {
    onUploaded: (data: DatasetUploadResponse) => setResult(data),
    onSuccess: (data: DatasetUploadResponse) => setResult(data),
    onUploadComplete: (data: DatasetUploadResponse) => setResult(data),
  };

  return (
    <main className="min-h-screen bg-[#121624] text-slate-100 px-6 py-10 selection:bg-[#00f0d2] selection:text-black font-sans">
      <div className="mx-auto max-w-5xl">
        {/* Top Header */}
        <div className="mb-8 flex items-center justify-between border-b border-white/10 pb-4">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400 hover:text-[#00f0d2] transition"
          >
            <ArrowLeft className="h-4 w-4" />
            NEXUS Home
          </Link>

          <div className="flex items-center gap-2 rounded-full border border-[#00f0d2]/30 bg-[#1a2138] px-3.5 py-1 text-xs font-bold text-[#00f0d2]">
            <span className="h-2 w-2 rounded-full bg-[#00f0d2] animate-pulse" />
            Autonomous Agent Mode Enabled
          </div>
        </div>

        {/* Page Title */}
        <div className="mb-10">
          <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-white">
            Autonomous <span className="text-[#00f0d2]">Analyst Workspace</span>
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Multi-step recursive investigation engine backed by deterministic DuckDB calculations.
          </p>
        </div>

        <div className="space-y-8">
          {result ? (
            <>
              {/* Dataset Profile */}
              <DatasetProfileDashboard
                dataset={result.dataset}
                profile={result.profile}
              />

              {/* Inquiry & Analyst Workspace */}
              <div className="rounded-3xl border border-white/10 bg-[#1a2035] p-6 shadow-2xl">
                <div className="flex items-center justify-between mb-3">
                  <h2 className="text-lg font-bold text-white flex items-center gap-2">
                    <Sparkles className="h-4 w-4 text-[#00f0d2]" />
                    Autonomous Investigation Loop
                  </h2>
                  <span className="text-xs text-[#00f0d2] font-mono font-medium">ReAct / Multi-Step Loop</span>
                </div>

                <p className="text-xs text-slate-400 mb-4">
                  Select a multi-step investigation scenario or provide a prompt:
                </p>

                {/* Suggested Chips */}
                <div className="mb-5 flex flex-wrap gap-2.5">
                  {SUGGESTED_QUESTIONS.map((item, idx) => (
                    <button
                      key={idx}
                      type="button"
                      disabled={loading}
                      onClick={() => executeAnalysis(item.query)}
                      className="flex items-center gap-2 rounded-xl border border-white/10 bg-[#222a44] px-3.5 py-2 text-xs font-semibold text-slate-200 shadow-sm transition hover:border-[#00f0d2] hover:bg-[#00f0d2]/10 hover:text-[#00f0d2] disabled:opacity-50"
                    >
                      <span>{item.icon}</span>
                      <span>{item.label}</span>
                    </button>
                  ))}
                </div>

                {/* Input Bar */}
                <form onSubmit={handleFormSubmit} className="flex gap-3">
                  <input
                    type="text"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="e.g. 'Why did profit collapse in Q2 and which products caused it?'"
                    className="flex-1 rounded-2xl border border-white/10 bg-[#121624] px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-[#00f0d2] focus:outline-none focus:ring-2 focus:ring-[#00f0d2]/20"
                  />
                  <button
                    type="submit"
                    disabled={loading || !prompt.trim()}
                    className="rounded-2xl bg-[#00f0d2] px-7 py-3 text-sm font-bold text-[#0e1322] transition hover:bg-[#42ffd8] hover:shadow-[0_0_20px_rgba(0,240,210,0.4)] disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {loading ? "Investigating..." : "Investigate"}
                  </button>
                </form>

                {/* Output Analysis Workspace */}
                {analysis && (
                  <div className="mt-8 space-y-6">
                    {/* Action Bar: PDF Export Button */}
                    <div className="flex items-center justify-between rounded-2xl border border-white/10 bg-[#151a2d] px-5 py-3 shadow-inner">
                      <span className="text-xs text-slate-400">
                        Investigation completed with verifiable evidence grounding.
                      </span>
                      <button
                        type="button"
                        onClick={handleExportPDF}
                        disabled={exporting}
                        className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-[#00f0d2] to-[#00bfa5] px-4 py-2 text-xs font-bold text-[#0c101c] transition hover:shadow-[0_0_20px_rgba(0,240,210,0.4)] disabled:opacity-50"
                      >
                        {exporting ? (
                          <>
                            <Loader2 className="h-3.5 w-3.5 animate-spin" />
                            Formatting PDF...
                          </>
                        ) : (
                          <>
                            <FileDown className="h-3.5 w-3.5" />
                            Export C-Suite PDF Report
                          </>
                        )}
                      </button>
                    </div>

                    {/* Investigation Trace */}
                    {analysis.trace && analysis.trace.length > 0 && (
                      <div className="rounded-2xl border border-white/10 bg-[#14192b] p-5 shadow-inner">
                        <div className="flex items-center justify-between mb-4 border-b border-white/5 pb-2">
                          <p className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                            <GitCommit className="h-4 w-4 text-[#00f0d2]" />
                            Agent Investigation Trace ({analysis.trace.length} Steps)
                          </p>
                          <span className="text-[10px] text-[#00f0d2] font-mono">100% Deterministic Evidence</span>
                        </div>

                        <div className="space-y-3">
                          {analysis.trace.map((t, idx) => (
                            <div
                              key={idx}
                              className="flex items-start gap-3 rounded-xl bg-[#1c233c]/60 p-3 border border-white/5 text-xs"
                            >
                              <div className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#00f0d2]/20 text-[#00f0d2] font-bold text-[10px]">
                                {idx + 1}
                              </div>
                              <div className="flex-1">
                                <div className="flex items-center justify-between">
                                  <span className="font-bold text-white">{t.step}</span>
                                  <span className="rounded bg-[#00f0d2]/10 px-2 py-0.5 font-mono text-[10px] text-[#00f0d2]">
                                    {t.tool}
                                  </span>
                                </div>
                                <p className="mt-1 text-slate-300 text-[11px] leading-relaxed">{t.action}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Executive Summary */}
                    <div className="rounded-2xl border border-[#00f0d2]/30 bg-gradient-to-br from-[#00f0d2]/15 via-[#1a223a] to-[#121624] p-5 shadow-lg">
                      <div className="flex items-center gap-2 text-[#00f0d2] text-xs font-bold uppercase tracking-wider mb-1">
                        <CheckCircle2 className="h-4 w-4" />
                        Autonomous Finding Summary
                      </div>
                      <p className="text-sm font-medium text-slate-100 leading-relaxed">
                        {analysis.summary_text}
                      </p>
                    </div>

                    {/* Metric Cards Grid */}
                    {analysis.findings && analysis.findings.length > 0 && (
                      <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3">
                        {analysis.findings.map((f, i) => (
                          <div
                            key={i}
                            className="rounded-2xl border border-white/10 bg-[#222a44] p-4 shadow-sm"
                          >
                            <p className="text-xs font-semibold text-slate-400">{f.title}</p>
                            <p className="mt-1 text-2xl font-black text-[#00f0d2]">{f.metric}</p>
                            <p className="mt-1 text-xs text-slate-300">{f.detail}</p>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Visual Chart */}
                    <div className="rounded-3xl border border-white/10 bg-[#161b2e] p-6 shadow-xl">
                      <AnalysisChart chart={analysis.chart} data={analysis.data} />
                    </div>

                    {/* Grounded Recommendations */}
                    {analysis.recommendations && analysis.recommendations.length > 0 && (
                      <div className="rounded-2xl border border-white/10 bg-[#161b2e] p-5 shadow-sm">
                        <h3 className="mb-3 text-xs font-bold uppercase tracking-wider text-[#00f0d2]">
                          Evidence-Grounded Action Directives
                        </h3>
                        <div className="space-y-3">
                          {analysis.recommendations.map((rec, i) => (
                            <div
                              key={i}
                              className="flex items-start gap-3 rounded-xl border border-white/5 bg-[#1f263e] p-3.5 text-sm"
                            >
                              <span
                                className={`rounded-lg px-2.5 py-1 text-[10px] font-black uppercase tracking-wider ${
                                  rec.priority === "High"
                                    ? "bg-rose-500/20 text-rose-400 border border-rose-500/30"
                                    : "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                                }`}
                              >
                                {rec.priority}
                              </span>
                              <div>
                                <p className="font-semibold text-white">{rec.action}</p>
                                <p className="mt-0.5 text-xs text-slate-400">{rec.reason}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="rounded-3xl border border-white/10 bg-[#1a2035] p-8 shadow-2xl">
              <UploadDropzone {...dropzoneProps} />
            </div>
          )}
        </div>
      </div>
    </main>
  );
}