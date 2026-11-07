"use client";

import { useAuth } from "@clerk/nextjs";
import { useCallback, useEffect, useState } from "react";
import { API_URL } from "@/types/lesson";
import type { UserProgress } from "@/types/progress";

interface ProgressResult {
  identity: string;
  requestVersion: number;
  progress: UserProgress | null;
  error: string | null;
}

export default function useUserProgress() {
  const { isLoaded, isSignedIn, userId, sessionId, getToken } = useAuth();
  const [result, setResult] = useState<ProgressResult | null>(null);
  const [requestVersion, setRequestVersion] = useState(0);
  const identity =
    isSignedIn && userId && sessionId ? `${userId}:${sessionId}` : null;

  useEffect(() => {
    if (!isLoaded || !identity) {
      return;
    }

    const controller = new AbortController();

    const fetchProgress = async () => {
      try {
        const token = await getToken();
        if (!token) {
          throw new Error("No session token available.");
        }

        const response = await fetch(`${API_URL}/me/progress`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          signal: controller.signal,
        });
        if (!response.ok) {
          throw new Error(
            `Could not load progress (HTTP ${response.status}).`,
          );
        }

        const progress: UserProgress = await response.json();
        if (!controller.signal.aborted) {
          setResult({
            identity,
            requestVersion,
            progress,
            error: null,
          });
        }
      } catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
          return;
        }

        if (!controller.signal.aborted) {
          setResult({
            identity,
            requestVersion,
            progress: null,
            error:
              error instanceof Error
                ? error.message
                : "Something went wrong while loading your progress.",
          });
        }
      }
    };

    void fetchProgress();
    return () => controller.abort();
  }, [getToken, identity, isLoaded, requestVersion]);

  const refetch = useCallback(() => {
    setRequestVersion((version) => version + 1);
  }, []);

  const hasCurrentResult =
    identity !== null &&
    result?.identity === identity &&
    result.requestVersion === requestVersion;

  return {
    progress: hasCurrentResult ? result.progress : null,
    loading: !isLoaded || (identity !== null && !hasCurrentResult),
    error: hasCurrentResult ? result.error : null,
    refetch,
  };
}
