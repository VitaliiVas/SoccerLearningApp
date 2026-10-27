import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Suspense } from "react";
import { ClerkProvider} from "@clerk/nextjs";
import Navbar, { SiteHeader } from "@/components/Navbar";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});



export const metadata: Metadata = {
  title: "Soccer Learning",
  description: "Build your soccer knowledge one lesson at a time.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-[#f5f7f2]">
        <ClerkProvider>
          <SiteHeader>
            <Suspense fallback={<div className="h-9 w-36" />}>
              <Navbar />
            </Suspense>
          </SiteHeader>
          {children}
        </ClerkProvider>
      </body>
    </html>
  );
}
