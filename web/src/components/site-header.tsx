import { ModeToggle } from "@/components/mode-toggle";
import { Button } from "@/components/ui/button";
import { ComingSoonButton } from "@/components/ui/coming-soon-button";
import Link from "next/link";

export const SiteHeader = () => {
  return (
    <header className="bg-background/95 supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50 w-full border-b backdrop-blur">
      <div className="container-wrapper">
        <div className="container flex h-16 items-center justify-between gap-2 md:gap-4">
          <div className="flex items-center gap-2">
            <span className="text-lg font-semibold">Summarize</span>
          </div>

          <div className="flex items-center gap-2">
            <ModeToggle />
            <ComingSoonButton variant="ghost">Sign In</ComingSoonButton>
            <Button asChild>
              <Link href="/auth/sign-up">Sign Up</Link>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};
