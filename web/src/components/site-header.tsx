"use client";

import { ModeToggle } from "@/components/mode-toggle";
import { Button } from "@/components/ui/button";
import { ComingSoonButton } from "@/components/ui/coming-soon-button";
import { AuthenticatedUser } from "@/features/users/types";
import { useBoundStore } from "@/stores";
import Link from "next/link";

export const SiteHeader = () => {
  const user = useBoundStore((state) => state.user);

  return (
    <header className="bg-background/95 supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50 w-full border-b backdrop-blur">
      <div className="container-wrapper">
        <div className="container flex h-16 items-center justify-between gap-2 md:gap-4">
          <div className="flex items-center gap-2">
            <span className="text-lg font-semibold">Summarize</span>
          </div>

          <div className="flex items-center gap-2">
            <ModeToggle />
            <SiteHeaderMenu user={user} />
          </div>
        </div>
      </div>
    </header>
  );
};

function UnauthenticatedMenu() {
  return (
    <>
      <Button asChild variant="ghost">
        <Link href="/auth/sign-in">Sign In</Link>
      </Button>
      <Button asChild>
        <Link href="/auth/sign-up">Sign Up</Link>
      </Button>
    </>
  );
}

function AuthenticatedMenu({ user }: { user: AuthenticatedUser }) {
  const logoutUser = useBoundStore((state) => state.logoutUser);

  return (
    <>
      <ComingSoonButton variant="ghost">Dashboard</ComingSoonButton>
      <ComingSoonButton variant="ghost">{user.name}</ComingSoonButton>
      <Button variant="outline" onClick={() => logoutUser()}>
        Sign Out
      </Button>
    </>
  );
}

function SiteHeaderMenu({ user }: { user: AuthenticatedUser | null }) {
  if (user === null) {
    return <UnauthenticatedMenu />;
  }

  return <AuthenticatedMenu user={user} />;
}
