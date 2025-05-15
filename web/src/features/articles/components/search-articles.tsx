"use client";
import { Card, CardContent } from "@/components/ui/card";
import { InputWithLoading } from "@/components/ui/input-with-loading";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useSearchArticles } from "@/features/articles/api";
import { useDebounce } from "@/hooks/use-debounce";
import { useCallback, useMemo, useState } from "react";

export const SearchArticles = () => {
  const [search, setSearch] = useState<string>("");
  const debouncedSearch = useDebounce(search, 300);

  const { data, isLoading, isError } = useSearchArticles(
    {
      name: debouncedSearch,
      page_index: 0,
      page_size: 9,
    },
    { enabled: !!debouncedSearch },
  );

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
  };

  const renderSearchResultCard = useCallback(() => {
    if (!debouncedSearch || isLoading) {
      return <></>;
    }

    if (isError || !data) {
      return (
        <Card>
          <CardContent>
            <p className="text-center text-sm text-red-500">
              An error occurred while fetching articles. Please try again.
            </p>
          </CardContent>
        </Card>
      );
    }

    if (!data.articles.length) {
      return (
        <Card>
          <CardContent>
            <p className="text-muted-foreground text-center text-sm">
              No articles found for &quot;{search}&quot;
            </p>
          </CardContent>
        </Card>
      );
    }

    return (
      <ScrollArea className="bg-card text-card-foreground flex max-h-64 flex-col gap-6 overflow-hidden rounded-xl border px-6 py-6 shadow-sm">
        <p className="text-muted-foreground text-center text-sm">
          Search Results
        </p>
        {data.articles.map((article) => (
          <div
            key={article.id}
            className="hover:bg-muted-foreground/10 cursor-pointer rounded-md p-2"
          >
            {article.name}
          </div>
        ))}
      </ScrollArea>
    );
  }, [debouncedSearch, isLoading, isError, data, search]);
  const SearchResultCard = useMemo(
    () => renderSearchResultCard,
    [renderSearchResultCard],
  );

  return (
    <div className="w-full max-w-3xl space-y-2 sm:space-y-4">
      <InputWithLoading
        className="h-14 rounded-lg border pr-12 pl-4 text-base shadow-sm"
        placeholder="Search existing articles"
        isLoading={!data && isLoading}
        value={search}
        onChange={onChange}
      />

      <SearchResultCard />
    </div>
  );
};
