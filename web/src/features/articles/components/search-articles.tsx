"use client";

import { InputWithLoading } from "@/components/ui/input-with-loading";
import { ScrollArea } from "@/components/ui/scroll-area";
import Link from "next/link";
import React, { Suspense, useState } from "react";
import { useInView } from "react-intersection-observer";
import { useQueryState } from "nuqs";
import {
  Popover,
  PopoverAnchor,
  PopoverContent,
} from "@/components/ui/popover";
import { useSearchArticles } from "@/features/articles/api/use-search-articles";
import { useDebounceCallback } from "@/hooks/use-debounce-callback";

export const SearchArticles = () => {
  return (
    <Suspense>
      <UnsuspendedSearchArticles />
    </Suspense>
  );
};

const UnsuspendedSearchArticles = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useQueryState("search", { defaultValue: "" });
  const [input, setInput] = useState(search);
  const debouncedSetSearch = useDebounceCallback(setSearch, 300);
  const { ref, inView } = useInView();

  const { data, status, isFetching, hasNextPage } = useSearchArticles(
    { title: search, page_size: 10 },
    inView,
  );

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
    debouncedSetSearch(e.target.value);
  };

  return (
    <div className="w-full max-w-3xl space-y-2 sm:space-y-4">
      <Popover open={isOpen}>
        <PopoverAnchor>
          <InputWithLoading
            inputClassName="h-14 rounded-lg border pr-12 pl-4 text-base shadow-sm"
            placeholder="Search existing articles from the database..."
            isLoading={isFetching}
            value={input}
            onChange={onChange}
            onFocus={() => setIsOpen(true)}
            onBlur={() => setIsOpen(false)}
          />
        </PopoverAnchor>
        <PopoverContent
          className="w-[var(--radix-popover-trigger-width)]"
          onOpenAutoFocus={(e) => e.preventDefault()}
        >
          {status === "pending" ? (
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
                {search ? "Search Results" : "Featured Articles"}
              </p>
              {data.pages.map((page, i) => (
                <React.Fragment key={i}>
                  {i === data.pages.length - 1 ? (
                    <div ref={ref} className="h-2"></div>
                  ) : null}
                  {page.articles.map((article) => (
                    <Link key={article.id} href={`/articles/${article.id}`}>
                      <div className="hover:bg-muted-foreground/10 cursor-pointer rounded-md p-2">
                        {article.title}
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
