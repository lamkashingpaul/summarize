"use client";

import { InputWithLoading } from "@/components/ui/input-with-loading";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useSearchArticles } from "@/features/articles/api";
import Link from "next/link";
import React, { useState } from "react";
import { useInView } from "react-intersection-observer";
import { useQueryState } from "nuqs";
import {
  Popover,
  PopoverAnchor,
  PopoverContent,
} from "@/components/ui/popover";
import { useDebounceCallback } from "@/hooks/use-debounce-callback";

export const SearchArticles = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useQueryState("search", { defaultValue: "" });
  const debouncedSetSearch = useDebounceCallback(setSearch, 500);
  const { ref, inView } = useInView();

  const { data, status, isFetching, hasNextPage } = useSearchArticles(
    { name: search, page_size: 10 },
    inView,
    { enabled: !!search },
  );

  return (
    <div className="w-full max-w-3xl space-y-2 sm:space-y-4">
      <Popover open={!!search && isOpen}>
        <PopoverAnchor>
          <InputWithLoading
            inputClassName="h-14 rounded-lg border pr-12 pl-4 text-base shadow-sm"
            placeholder="Search existing articles from the database..."
            isLoading={isFetching}
            onChange={(e) => debouncedSetSearch(e.target.value)}
            onFocus={() => setIsOpen(true)}
            onBlur={() => setIsOpen(false)}
          />
        </PopoverAnchor>
        <PopoverContent
          className="w-[var(--radix-popover-trigger-width)]"
          onOpenAutoFocus={(e) => e.preventDefault()}
        >
          {!search || status === "pending" ? (
            <></>
          ) : status === "error" ? (
            <p className="text-center text-sm text-red-500">
              An error occurred while fetching articles. Please try again.
            </p>
          ) : !data.pages.length || data.pages[0].articles_total_count === 0 ? (
            <p className="text-muted-foreground text-center text-sm break-all">
              No articles found for &quot;{search}&quot;
            </p>
          ) : (
            <ScrollArea className="flex max-h-64 flex-col">
              <p className="text-muted-foreground text-center text-sm">
                Search Results
              </p>
              {data.pages.map((page, i) => (
                <React.Fragment key={i}>
                  {i === data.pages.length - 1 ? (
                    <div ref={ref} className="h-2"></div>
                  ) : null}
                  {page.articles.map((article) => (
                    <Link key={article.id} href={`/articles/${article.id}`}>
                      <div className="hover:bg-muted-foreground/10 cursor-pointer rounded-md p-2">
                        {article.name}
                      </div>
                    </Link>
                  ))}
                </React.Fragment>
              ))}
              {hasNextPage ? (
                <div className="text-muted-foreground text-center text-sm">
                  Loading more results...
                </div>
              ) : null}
            </ScrollArea>
          )}
        </PopoverContent>
      </Popover>
    </div>
  );
};
