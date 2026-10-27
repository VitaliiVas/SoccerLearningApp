export interface Lesson {
    id: number;
    title: string;
    description: string | null;
    content: string;
    xp_reward: number;
}

export const API_URL =
    process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
