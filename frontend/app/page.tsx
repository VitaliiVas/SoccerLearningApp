"use client";

import { API_URL, type Lesson } from "@/types/lesson";
import LessonCard from "@/components/LessonCard";
import { useEffect, useState } from "react";

export default function HomePage() {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    const controller = new AbortController();

    const fetchLessons = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`${API_URL}/lessons`, {
          signal: controller.signal,
        });
        if (!response.ok) {
          throw new Error(`Could not load lessons (HTTP ${response.status}).`);
        }

        const data: Lesson[] = await response.json();
        setLessons(data);
      } catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
          return;
        }

        setError(
          error instanceof Error
            ? error.message
            : "Something went wrong while loading lessons.",
        );
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    void fetchLessons();
    return () => controller.abort();
  }, [retryCount]);

  return (
    <main className="flex-1 bg-[#f5f7f2] px-5 py-12 text-slate-900 sm:px-8 sm:py-16">
      <div className="mx-auto max-w-6xl">
        <header className="mb-10 border-b border-slate-200 pb-8">
          <p className="mb-3 text-sm font-bold uppercase tracking-[0.2em] text-emerald-700">
            Learn the game
          </p>
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            Soccer Learning
          </h1>
          <p className="mt-4 max-w-2xl text-lg leading-8 text-slate-600">
            Build your soccer knowledge one lesson at a time. Pick a lesson and
            get started.
          </p>
        </header>

        <section aria-labelledby="lessons-heading">
          <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
            <h2 id="lessons-heading" className="text-2xl font-bold">
              Lessons
            </h2>
            {!loading && !error && (
              <p className="text-sm text-slate-600">
                {lessons.length} {lessons.length === 1 ? "lesson" : "lessons"}
              </p>
            )}
          </div>

          {loading && (
            <p role="status" className="rounded-xl bg-white p-6 text-slate-600 shadow-sm">
              Loading lessons…
            </p>
          )}

          {error && (
            <div
              role="alert"
              className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-800"
            >
              <p className="font-semibold">Lessons couldn’t be loaded.</p>
              <p className="mt-1 text-sm">{error}</p>
              <p className="mt-2 text-sm">
                Make sure the learning API is running, then try again.
              </p>
              <button
                type="button"
                onClick={() => setRetryCount((count) => count + 1)}
                className="mt-4 rounded-lg bg-red-800 px-4 py-2 text-sm font-semibold text-white transition hover:bg-red-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-800"
              >
                Try again
              </button>
            </div>
          )}

          {!loading && !error && lessons.length === 0 && (
            <p className="rounded-xl bg-white p-6 text-slate-600 shadow-sm">
              No lessons are available yet. Check back soon.
            </p>
          )}

          {!loading && !error && lessons.length > 0 && (
            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {lessons.map((lesson) => (
                <LessonCard key={lesson.id} lesson={lesson} />
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}