"use client";

import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";
import { API_URL } from "@/types/lesson";

interface Me {
  user_id: string;
}

export default function CurrentUser() {
  const { isLoaded, isSignedIn, getToken } = useAuth();
  const [me, setMe] = useState<Me | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isLoaded || !isSignedIn) {
      return;
    }

    const controller = new AbortController();

    const fetchMe = async () => {
      setError(null);

      try {
        const token = await getToken();
        if (!token) {
          throw new Error("No session token available.");
        }

        const response = await fetch(`${API_URL}/me`, {
          headers: { Authorization: `Bearer ${token}` },
          signal: controller.signal,
        });
        if (!response.ok) {
          throw new Error(`Could not load profile (HTTP ${response.status}).`);
        }

        const data: Me = await response.json();
        setMe(data);
      } catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
          return;
        }

        setError(
          error instanceof Error
            ? error.message
            : "Something went wrong while loading your profile.",
        );
      }
    };

    fetchMe();

    return () => controller.abort();
  }, [isLoaded, isSignedIn, getToken]);

  if (error) {
    return (
      <span className="text-xs text-red-700" role="status">
        {error}
      </span>
    );
  }

  if (!me) {
    return null;
  }

  return (
    <span className="hidden text-xs text-slate-500 sm:inline" title={me.user_id}>
      {me.user_id}
    </span>
  );
}
