import { searchArticlesQuerySchema } from "@/features/articles/schemas";
import { SearchArticlesResponse } from "@/features/articles/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/lib/react-query";
import { useQuery, UseQueryOptions } from "@tanstack/react-query";
import { z } from "zod";

type SearchArticlesQueryDto = z.input<typeof searchArticlesQuerySchema>;
type SearchArticlesResponseData = SearchArticlesResponse;
type UseSearchArticlesOptions = Omit<
  UseQueryOptions<SearchArticlesResponseData, ReactQueryError>,
  "queryKey" | "queryFn"
>;

const searchArticles = async (query: SearchArticlesQueryDto) => {
  const response = await customFetch<SearchArticlesResponseData>({
    url: "/articles",
    params: query,
  });
  return response.data;
};

export const useSearchArticles = (
  query: SearchArticlesQueryDto,
  options?: UseSearchArticlesOptions,
) => {
  const q = useQuery<SearchArticlesResponseData, ReactQueryError>({
    queryKey: ["articles", query],
    queryFn: () => searchArticles(query),
    ...options,
  });

  return q;
};
