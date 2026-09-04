"use client";

import React from "react";
import Link from "next/link";
import { 
  ArrowRight, 
  Sparkles, 
  TrendingUp, 
  Database, 
  BarChart3, 
  ShieldCheck,
  Activity,
  Layers,
  Cpu,
  Workflow
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="relative min-h-screen bg-[#121624] text-slate-100 selection:bg-[#00f0d2] selection:text-black font-sans overflow-x-hidden">
      {/* Ambient Neon Cyan Background Glows */}
      <div className="pointer-events-none absolute inset-0 z-0">
        <div className="absolute top-1/4 left-1/2 h-[450px] w-[700px] -translate-x-1/2 rounded-full bg-[#00f0d2]/10 blur-[130px]" />
        <div className="absolute -top-20 left-1/4 h-[350px] w-[400px] rounded-full bg-[#1b254b]/50 blur-[100px]" />
        <div className="absolute bottom-10 right-1/4 h-[300px] w-[400px] rounded-full bg-[#00f0d2]/5 blur-[120px]" />
      </div>

      {/* Top Floating App Bar */}
      <header className="relative z-20 mx-auto flex max-w-6xl items-center justify-between px-6 pt-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#00f0d2] text-[#121624] shadow-[0_0_20px_rgba(0,240,210,0.4)] font-black text-lg">
            N
          </div>
          <span className="text-xl font-bold tracking-wider text-white">
            NEXUS <span className="text-[#00f0d2] font-normal">BI</span>
          </span>
        </div>

        {/* Center Pill Navigation */}
        <nav className="hidden md:flex items-center gap-2 rounded-full border border-white/10 bg-[#1e243b]/70 px-5 py-2 backdrop-blur-xl text-xs font-medium text-slate-300 shadow-lg">
          <Link href="/dashboard" className="px-3 py-1 text-white hover:text-[#00f0d2] transition">Overview</Link>
          <span className="text-white/20">•</span>
          <Link href="/dashboard" className="px-3 py-1 hover:text-[#00f0d2] transition">Investigation Loop</Link>
          <span className="text-white/20">•</span>
          <Link href="/dashboard" className="px-3 py-1 hover:text-[#00f0d2] transition">Evidence Grounding</Link>
        </nav>

        <div className="flex items-center gap-3">
          <Link
            href="/dashboard"
            className="rounded-full bg-[#00f0d2] px-5 py-2.5 text-xs font-bold text-[#0e1322] transition-all duration-300 hover:bg-[#38ffd9] hover:shadow-[0_0_25px_rgba(0,240,210,0.5)] transform hover:-translate-y-0.5"
          >
            Launch Analyst →
          </Link>
        </div>
      </header>

      {/* Centered Hero Showcase */}
      <main className="relative z-10 mx-auto max-w-6xl px-6 pt-16 pb-24 text-center">
        {/* Feature Badge */}
        <div className="inline-flex items-center gap-2 rounded-full border border-[#00f0d2]/30 bg-[#1a233d] px-4 py-1.5 text-xs font-semibold text-[#00f0d2] shadow-[0_0_15px_rgba(0,240,210,0.15)] mb-8">
          <Sparkles className="h-3.5 w-3.5" />
          Autonomous Business Intelligence Engine
        </div>

        {/* Central Focus: NEXUS BI */}
        <div className="relative inline-block mb-4">
          <h1 className="text-6xl sm:text-8xl md:text-9xl font-black tracking-tight text-white uppercase drop-shadow-[0_15px_35px_rgba(0,0,0,0.8)]">
            NEXUS <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#00f0d2] via-[#46ffd3] to-[#00bfa5] drop-shadow-[0_0_35px_rgba(0,240,210,0.4)]">BI</span>
          </h1>
          <p className="mt-2 text-sm sm:text-base font-semibold tracking-[0.3em] uppercase text-[#00f0d2]/90">
            Ask a question. NEXUS investigates.
          </p>
        </div>

        <p className="mx-auto max-w-2xl text-base sm:text-lg text-slate-400 font-light leading-relaxed mb-10">
          Upload any CSV or Excel file to execute multi-step investigation loops, deterministic DuckDB calculations, and evidence-grounded action plans without code generation risks.
        </p>

        {/* Primary Action Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 mb-20">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 rounded-2xl bg-[#00f0d2] px-8 py-4 text-sm font-bold text-[#0c101c] transition duration-300 hover:bg-[#46ffd3] hover:shadow-[0_0_30px_rgba(0,240,210,0.4)] transform hover:-translate-y-1"
          >
            Start Investigation
            <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            href="/dashboard"
            className="flex items-center gap-2 rounded-2xl border border-white/10 bg-[#1f263f] px-8 py-4 text-sm font-medium text-slate-200 transition duration-300 hover:border-[#00f0d2]/40 hover:bg-[#252e4c] hover:text-white shadow-lg"
          >
            Upload Datasets
          </Link>
        </div>

        {/* 3 Architecture & Capabilities Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto text-left">
          
          {/* Card 1: Data Health & Ingestion Pipeline */}
          <div className="rounded-3xl border border-white/10 bg-[#1a2035] p-5 shadow-2xl backdrop-blur-xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2.5">
                  <div className="h-8 w-8 rounded-full bg-[#00f0d2]/20 border border-[#00f0d2] flex items-center justify-center text-[#00f0d2]">
                    <Activity className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="text-xs font-bold text-white">Ingestion Layer</p>
                    <p className="text-[10px] text-slate-400">Automated Profiling</p>
                  </div>
                </div>
                <div className="h-5 w-6 rounded flex flex-col justify-between py-1 px-1 bg-white/5">
                  <div className="h-0.5 bg-white/40 rounded" />
                  <div className="h-0.5 bg-white/40 rounded" />
                  <div className="h-0.5 bg-white/40 rounded" />
                </div>
              </div>

              {/* Cyan Geometric Highlight Card */}
              <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-[#00f0d2] to-[#00bfa5] p-5 text-[#0b101d] shadow-lg mb-4">
                <div className="absolute -right-4 -bottom-6 w-24 h-24 rounded-full bg-white/20 blur-sm" />
                <p className="text-[11px] font-bold uppercase tracking-wider text-[#0b101d]/80">Data Quality Audit</p>
                <div className="mt-2 flex items-baseline justify-between">
                  <span className="text-3xl font-black">100/100</span>
                  <span className="rounded-full bg-[#0b101d]/15 px-2.5 py-1 text-[10px] font-bold">Standard</span>
                </div>
                <p className="mt-2 text-[10px] font-medium opacity-90">Automated schema, null, and duplicate checks</p>
              </div>

              {/* 2x2 Feature Mini-Grid */}
              <div className="grid grid-cols-2 gap-2.5">
                <div className="rounded-xl bg-[#222a44] p-3 border border-white/5">
                  <Database className="h-4 w-4 text-[#00f0d2] mb-1.5" />
                  <p className="text-xs font-semibold text-white">DuckDB</p>
                  <p className="text-[10px] text-slate-400">In-Memory Engine</p>
                </div>
                <div className="rounded-xl bg-[#222a44] p-3 border border-white/5">
                  <ShieldCheck className="h-4 w-4 text-[#00f0d2] mb-1.5" />
                  <p className="text-xs font-semibold text-white">Deterministic</p>
                  <p className="text-[10px] text-slate-400">Zero Hallucination</p>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-white/5 flex justify-center">
              <div className="h-10 w-10 rounded-full bg-[#00f0d2] flex items-center justify-center text-[#121624] shadow-[0_0_15px_rgba(0,240,210,0.4)]">
                <TrendingUp className="h-5 w-5" />
              </div>
            </div>
          </div>

          {/* Card 2: Autonomous Investigation Loop */}
          <div className="rounded-3xl border border-[#00f0d2]/30 bg-[#1a2035] p-5 shadow-[0_0_30px_rgba(0,240,210,0.15)] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className="h-7 w-7 rounded-full bg-[#00f0d2] text-[#121624] flex items-center justify-center font-bold text-xs">
                    <Workflow className="h-4 w-4" />
                  </div>
                  <span className="text-xs font-bold text-white">Investigation Loop</span>
                </div>
                <span className="text-[11px] text-[#00f0d2] font-semibold">Multi-Step</span>
              </div>

              <div className="text-center py-2">
                <span className="text-2xl font-extrabold text-white tracking-tight">Recursive Analysis</span>
                <div className="mt-1 flex items-center justify-center gap-2 text-xs text-slate-400">
                  <span>Plan → Execute → Audit → Explain</span>
                </div>
              </div>

              {/* Graphical Wave Preview */}
              <div className="mt-3 rounded-2xl bg-[#222a44] p-4 border border-white/5 relative overflow-hidden">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-[11px] font-semibold text-slate-300">Evidence Curve</span>
                  <span className="text-xs font-bold text-[#00f0d2]">Calculated</span>
                </div>
                <div className="h-24 w-full flex items-end">
                  <svg viewBox="0 0 100 45" className="w-full h-full overflow-visible">
                    <defs>
                      <linearGradient id="cyanGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#00f0d2" stopOpacity="0.5" />
                        <stop offset="100%" stopColor="#00f0d2" stopOpacity="0.0" />
                      </linearGradient>
                    </defs>
                    <path
                      d="M0,35 Q20,10 40,25 T80,8 T100,20 L100,45 L0,45 Z"
                      fill="url(#cyanGrad)"
                    />
                    <path
                      d="M0,35 Q20,10 40,25 T80,8 T100,20"
                      fill="none"
                      stroke="#00f0d2"
                      strokeWidth="2.5"
                    />
                    <circle cx="80" cy="8" r="3.5" fill="#00f0d2" />
                  </svg>
                </div>
                <div className="flex justify-between text-[9px] font-mono text-slate-400 mt-2">
                  <span>Step 1</span>
                  <span>Step 2</span>
                  <span>Step 3</span>
                  <span>Synthesis</span>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-white/5 flex justify-center">
              <div className="h-10 w-10 rounded-full bg-[#00f0d2] flex items-center justify-center text-[#121624] shadow-[0_0_15px_rgba(0,240,210,0.4)]">
                <Layers className="h-5 w-5" />
              </div>
            </div>
          </div>

          {/* Card 3: Deterministic Action Directives */}
          <div className="rounded-3xl border border-white/10 bg-[#1a2035] p-5 shadow-2xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold text-white">Decision Engine</span>
                <span className="rounded-md bg-[#232c48] px-2 py-0.5 text-[10px] font-bold text-[#00f0d2]">Grounded</span>
              </div>

              {/* Cyan Top Banner */}
              <div className="rounded-2xl bg-[#00f0d2] p-4 text-[#0f1424] font-bold mb-4 shadow-lg">
                <div className="flex justify-between items-center text-xs">
                  <span>ROOT-CAUSE DETECTION</span>
                  <span className="rounded-full bg-black/15 px-2 py-0.5 text-[9px]">ACTIVE</span>
                </div>
                <p className="mt-2 text-sm font-black leading-snug">
                  Autonomous correlation identifies contributing factors and anomalies
                </p>
              </div>

              {/* Signal Bar Graphic */}
              <div className="rounded-2xl bg-[#222a44] p-4 border border-white/5">
                <div className="flex items-end justify-between gap-1.5 h-16">
                  {[20, 50, 35, 80, 45, 95, 60, 100, 75, 40, 85, 30].map((h, i) => (
                    <div
                      key={i}
                      className="w-full rounded-t-sm"
                      style={{
                        height: `${h}%`,
                        backgroundColor: i === 7 ? "#00f0d2" : "rgba(0, 240, 210, 0.35)",
                        boxShadow: i === 7 ? "0 0 10px #00f0d2" : "none"
                      }}
                    />
                  ))}
                </div>
                <div className="flex justify-between text-[9px] font-mono text-slate-400 mt-2">
                  <span>Input</span>
                  <span>Validation</span>
                  <span>Analysis</span>
                  <span className="text-[#00f0d2]">Decide</span>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-white/5 flex justify-center">
              <div className="h-10 w-10 rounded-full bg-[#00f0d2] flex items-center justify-center text-[#121624] shadow-[0_0_15px_rgba(0,240,210,0.4)]">
                <BarChart3 className="h-5 w-5" />
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}