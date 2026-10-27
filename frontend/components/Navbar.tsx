import Link from "next/link";
import { Show, SignInButton, SignUpButton, UserButton } from "@clerk/nextjs";
import AuthTest from "@/components/AuthTest";
import CurrentUser from "@/components/CurrentUser";

export default function Navbar() {
  return (
    <nav className="flex items-center gap-3">
      <Show when="signed-out">
        <SignInButton>
          <button
            type="button"
            className="rounded-lg px-4 py-2 text-sm font-semibold text-emerald-800 transition hover:bg-emerald-50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-800"
          >
            Sign in
          </button>
        </SignInButton>
        <SignUpButton>
          <button
            type="button"
            className="rounded-lg bg-emerald-700 px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-800"
          >
            Sign up
          </button>
        </SignUpButton>
      </Show>

      <Show when="signed-in">
        <AuthTest />
        <CurrentUser />
        <UserButton />
      </Show>
    </nav>
  );
}

export function SiteHeader({ children }: { children: React.ReactNode }) {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-5 sm:px-8">
        <Link
          href="/"
          className="rounded-lg text-lg font-bold tracking-tight text-slate-900 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-emerald-800"
        >
          <span aria-hidden="true">⚽</span> Soccer Learning
        </Link>
        {children}
      </div>
    </header>
  );
}
