"use client";

import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";
import { API_URL } from "@/types/lesson";

export default function AuthTest() {
  const { isLoaded, isSignedIn, getToken } = useAuth();
  const [token, setToken] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  useEffect(() => {
    if (!isLoaded || !isSignedIn) {
      return;
    }

    const controller = new AbortController();

    const runTest = async () => {
      try {
        const token = await getToken();
        if (!token) {
          throw new Error("No authentication token available.");
        }
        setToken(token);

        const response = await fetch(`${API_URL}/me`, {
          headers: { Authorization: `Bearer ${token}` },
          signal: controller.signal,
        });
        const body = await response.json();
        setResult(`${response.status} ${JSON.stringify(body)}`);
      } catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
          return;
        }

        setResult(error instanceof Error ? error.message : "Request failed.");
      }
    };

    runTest();

    return () => controller.abort();
  }, [isLoaded, isSignedIn, getToken]);

  return (
    <div className="flex flex-col text-[11px] leading-tight text-slate-500">
      <span>Signed in: {isSignedIn ? "Yes" : "No"}</span>
      <span className="max-w-48 truncate" title={token ?? undefined}>
        Token: {token ?? "—"}
      </span>
      <span className="max-w-48 truncate" title={result ?? undefined}>
        /me: {result ?? "…"}
      </span>
    </div>
  );
}
