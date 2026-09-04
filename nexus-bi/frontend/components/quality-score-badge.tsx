interface QualityScoreBadgeProps {
  score: number; // 0-100
}

function tierFor(score: number): { label: string; className: string } {
  if (score >= 85) return { label: "Excellent", className: "bg-mint/15 text-mint border-mint/30" };
  if (score >= 65)
    return { label: "Good", className: "bg-amber-500/15 text-amber-500 border-amber-500/30" };
  return { label: "Needs attention", className: "bg-red-500/15 text-red-500 border-red-500/30" };
}

export function QualityScoreBadge({ score }: QualityScoreBadgeProps) {
  const tier = tierFor(score);
  return (
    <div className="rounded-panel border border-border bg-navy/[0.02] p-5 dark:bg-white/[0.02]">
      <p className="text-xs uppercase tracking-wide text-muted">Quality Score</p>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-2xl font-semibold">{score.toFixed(1)}</span>
        <span className="text-sm text-muted">/ 100</span>
      </div>
      <span
        className={`mt-2 inline-block rounded-full border px-2 py-0.5 text-xs font-medium ${tier.className}`}
      >
        {tier.label}
      </span>
    </div>
  );
}
