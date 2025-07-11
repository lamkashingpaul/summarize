"use client";

import { Loader } from "@/components/loader";
import { ModeToggle } from "@/components/mode-toggle";
import { Button } from "@/components/ui/button";
import { ComingSoonButton } from "@/components/ui/coming-soon-button";
import { AuthenticatedUser } from "@/features/users/types";
import { useBoundStore, useStore } from "@/stores";
import { motion, AnimatePresence } from "motion/react";
import Link from "next/link";

type SiteHeaderMenuProps = {
  user?: AuthenticatedUser | null;
};

export const SiteHeader = () => {
  const user = useStore(useBoundStore, (state) => state.user);

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
    <div className="flex flex-nowrap items-center gap-2">
      <Button asChild variant="ghost">
        <Link href="/auth/sign-in">Sign In</Link>
      </Button>
      <Button asChild>
        <Link href="/auth/sign-up">Sign Up</Link>
      </Button>
    </div>
  );
}

function AuthenticatedMenu({ user }: { user: AuthenticatedUser }) {
  const logoutUser = useBoundStore((state) => state.logoutUser);

  return (
    <div className="flex flex-nowrap items-center gap-2">
      <ComingSoonButton variant="ghost">Dashboard</ComingSoonButton>
      <ComingSoonButton variant="ghost">{user.name}</ComingSoonButton>
      <Button variant="outline" onClick={() => logoutUser()}>
        Sign Out
      </Button>
    </div>
  );
}

function SiteHeaderMenu(props: SiteHeaderMenuProps) {
  const { user } = props;

  const motionKey =
    user === undefined
      ? "hydrating"
      : user
        ? "authenticated"
        : "unauthenticated";

  const menu =
    user === undefined ? (
      <Loader className="size-4 border-2" />
    ) : user ? (
      <AuthenticatedMenu user={user} />
    ) : (
      <UnauthenticatedMenu />
    );

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={motionKey}
        initial={{ width: "auto" }}
        animate={{ width: "auto" }}
        exit={{ width: 0 }}
        transition={{ duration: 0.2, ease: "easeInOut" }}
      >
        {menu}
      </motion.div>
    </AnimatePresence>
  );
}
