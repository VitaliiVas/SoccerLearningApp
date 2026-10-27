import Link from "next/link";
import type { Lesson } from "@/types/lesson";

function LessonCard({ lesson }: { lesson: Lesson }) {
    return (
        <Link
            href={`/lessons/${lesson.id}`}
            className="group block h-full rounded-2xl focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-emerald-800"
        >
            <article className="flex h-full flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition group-hover:-translate-y-1 group-hover:shadow-md">
                <h3 className="text-xl font-bold text-slate-900">{lesson.title}</h3>
                <p className="mt-3 flex-1 leading-7 text-slate-600">
                    {lesson.description ?? "No description yet."}
                </p>
                <p className="mt-6 w-fit rounded-full bg-emerald-50 px-3 py-1 text-sm font-semibold text-emerald-800">
                    {lesson.xp_reward} XP
                </p>
            </article>
        </Link>
    );
}

export default LessonCard;
