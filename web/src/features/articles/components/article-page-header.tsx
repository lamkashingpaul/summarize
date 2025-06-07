import { ComingSoonButton } from "@/components/ui/coming-soon-button";
import { ArrowLeft, Bookmark, Download, Share2 } from "lucide-react";
import Link from "next/link";

export const ArticlePageHeader = () => {
  return (
    <header className="bg-background/95 supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50 w-full border-b backdrop-blur">
      <div className="container-wrapper">
        <div className="container flex h-16 items-center justify-between gap-2 md:gap-4">
          <div className="flex items-center gap-2">
            <Link
              href="/"
              className="text-muted-foreground hover:text-foreground flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back to search</span>
            </Link>
          </div>

          <div className="flex items-center gap-2">
            <ComingSoonButton variant="ghost" size="icon">
              <Share2 className="h-4 w-4" />
            </ComingSoonButton>
            <ComingSoonButton variant="ghost" size="icon">
              <Bookmark className="h-4 w-4" />
            </ComingSoonButton>
            <ComingSoonButton variant="ghost" size="icon">
              <Download className="h-4 w-4" />
            </ComingSoonButton>
          </div>
        </div>
      </div>
    </header>
  );
};
