"use client";
import { SlideIn } from "@/components/slide-in";
import { Card, CardContent } from "@/components/ui/card";
import { InputWithLoading } from "@/components/ui/input-with-loading";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useSearchArticles } from "@/features/articles/api";
import { useDebounce } from "@/hooks/use-debounce";
import { AnimatePresence } from "motion/react";
import React, { useState } from "react";
import { useInView } from "react-intersection-observer";

export const SearchArticles = () => {
  const [search, setSearch] = useState<string>("");
  const debouncedSearch = useDebounce(search, 300);
  const { ref, inView } = useInView();

  const { data, status, isFetching, hasNextPage } = useSearchArticles(
    { name: debouncedSearch, page_size: 10 },
    inView,
    { enabled: !!debouncedSearch },
  );

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
  };

  return (
    <div className="w-full max-w-3xl space-y-2 sm:space-y-4">
      <InputWithLoading
        className="h-14 rounded-lg border pr-12 pl-4 text-base shadow-sm"
        placeholder="Search existing articles"
        isLoading={isFetching}
        value={search}
        onChange={onChange}
      />

      <AnimatePresence>
        {debouncedSearch && (
          <SlideIn>
            {!debouncedSearch || status === "pending" ? (
              <></>
            ) : status === "error" ? (
              <Card>
                <CardContent>
                  <p className="text-center text-sm text-red-500">
                    An error occurred while fetching articles. Please try again.
                  </p>
                </CardContent>
              </Card>
            ) : !data.pages.length ||
              data.pages[0].articles_total_count === 0 ? (
              <Card>
                <CardContent>
                  <p className="text-muted-foreground text-center text-sm">
                    No articles found for &quot;{search}&quot;
                  </p>
                </CardContent>
              </Card>
            ) : (
              <ScrollArea className="bg-card text-card-foreground flex max-h-64 flex-col gap-6 overflow-hidden rounded-xl border px-6 py-6 shadow-sm">
                <p className="text-muted-foreground text-center text-sm">
                  Search Results
                </p>
                {data.pages.map((page, i) => (
                  <React.Fragment key={i}>
                    {i === data.pages.length - 1 ? (
                      <div ref={ref} className="h-2"></div>
                    ) : null}
                    {page.articles.map((article) => (
                      <div
                        key={article.id}
                        className="hover:bg-muted-foreground/10 cursor-pointer rounded-md p-2"
                      >
                        {article.name}
                      </div>
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
          </SlideIn>
        )}
      </AnimatePresence>
    </div>
  );
};
