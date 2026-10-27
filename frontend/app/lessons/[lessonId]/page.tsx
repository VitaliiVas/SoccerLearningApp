"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import { API_URL, type Lesson } from "@/types/lesson";

function LessonContent() {
  const { lessonId } = useParams<{ lessonId: string }>();
  const id = Number(lessonId);
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const isValidId = Number.isInteger(id) && id > 0;

  useEffect(() => {
    if (!isValidId) {
      return;
    }

    const controller = new AbortController();

    const fetchLesson = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`${API_URL}/lessons/${id}`, {
          signal: controller.signal,
        });
        if (!response.ok) {
          throw new Error(
            response.status === 404
              ? "This lesson could not be found."
              : `Could not load lesson (HTTP ${response.status}).`,
          );
        }

        const lessonData: Lesson = await response.json();
        setLesson(lessonData);
      } catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
          return;
        }

        setError(
          error instanceof Error
            ? error.message
            : "Something went wrong while loading this lesson.",
        );
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    void fetchLesson();
    return () => controller.abort();
  }, [id, isValidId, retryCount]);

  return (
    <main className="flex-1 bg-[#f5f7f2] px-5 py-12 text-slate-900 sm:px-8 sm:py-16">
      <article className="mx-auto max-w-3xl">
        <Link
          href="/"
          className="inline-flex items-center gap-2 rounded-lg font-semibold text-emerald-800 hover:text-emerald-950 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-emerald-800"
        >
          <span aria-hidden="true">←</span> All lessons
        </Link>

        {!isValidId && (
          <section
            role="alert"
            className="mt-8 rounded-2xl border border-amber-200 bg-white p-8 shadow-sm"
          >
            <h1 className="text-2xl font-bold">Invalid lesson</h1>
            <p className="mt-2 leading-7 text-slate-600">
              The lesson ID must be a positive integer.
            </p>
          </section>
        )}

        {isValidId && loading && (
          <p
            role="status"
            className="mt-8 rounded-2xl bg-white p-8 text-slate-600 shadow-sm"
          >
            Loading lesson…
          </p>
        )}

        {isValidId && error && (
          <section
            role="alert"
            className="mt-8 rounded-2xl border border-red-200 bg-red-50 p-8 text-red-800"
          >
            <h1 className="text-2xl font-bold">Lesson unavailable</h1>
            <p className="mt-2">{error}</p>
            <p className="mt-2 text-sm">
              Make sure the learning API is running, then try again.
            </p>
            <button
              type="button"
              onClick={() => setRetryCount((count) => count + 1)}
              className="mt-5 rounded-lg bg-red-800 px-4 py-2 text-sm font-semibold text-white transition hover:bg-red-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-800"
            >
              Try again
            </button>
          </section>
        )}

        {isValidId && !loading && !error && lesson && (
          <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-7 shadow-sm sm:p-10">
            <p className="text-sm font-bold uppercase tracking-[0.2em] text-emerald-700">
              Soccer lesson
            </p>
            <h1 className="mt-3 text-3xl font-bold tracking-tight sm:text-4xl">
              {lesson.title}
            </h1>
            {lesson.description && (
              <p className="mt-4 text-lg leading-8 text-slate-600">
                {lesson.description}
              </p>
            )}
            <div className="my-8 h-px bg-slate-200" />
            <div className="whitespace-pre-wrap leading-8 text-slate-800">
              {lesson.content}
            </div>
            <p className="mt-8 inline-flex rounded-full bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-800">
              Reward: {lesson.xp_reward} XP
            </p>
          </section>
        )}
      </article>
    </main>
  );
}

export default function LessonPage() {
  return (
    <Suspense
      fallback={
        <main className="flex-1 bg-[#f5f7f2] px-5 py-12 text-slate-900 sm:px-8 sm:py-16">
          <div
            role="status"
            className="mx-auto max-w-3xl rounded-2xl bg-white p-8 text-slate-600 shadow-sm"
          >
            Loading lesson…
          </div>
        </main>
      }
    >
      <LessonContent />
    </Suspense>
  );
}
