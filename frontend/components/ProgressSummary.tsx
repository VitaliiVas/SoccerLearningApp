"use client";

import type { UserProgress } from "@/types/progress";

interface ProgressSummaryProps {
  progress: UserProgress | null;
}

export default function ProgressSummary({ progress }: ProgressSummaryProps) {
  if (progress === null) {
    return null;
  }

  return (
    <section
      aria-labelledby="progress-heading"
      className="mb-8 rounded-xl border border-emerald-100 bg-white p-6 shadow-sm"
    >
      <h2
        id="progress-heading"
        className="text-sm font-bold uppercase tracking-[0.2em] text-emerald-700"
      >
        Your progress
      </h2>
      <div className="mt-4 flex flex-wrap gap-x-8 gap-y-3 text-slate-700">
        <p>
          <span aria-hidden="true">⭐</span> Total XP:{" "}
          <span className="font-semibold">{progress.total_xp}</span>
        </p>
        <p>
          <span aria-hidden="true">✅</span> Completed lessons:{" "}
          <span className="font-semibold">{progress.total_completed}</span>
        </p>
      </div>
    </section>
  );
}
