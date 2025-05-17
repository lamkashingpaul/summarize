import { searchArticlesQuerySchema } from "@/features/articles/schemas";
import { SearchArticlesResponse } from "@/features/articles/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/lib/react-query";
import {
  InfiniteData,
  QueryKey,
  useInfiniteQuery,
  UseInfiniteQueryOptions,
} from "@tanstack/react-query";
import { useEffect } from "react";
import { z } from "zod";

type SearchArticlesQueryDto = z.input<typeof searchArticlesQuerySchema>;
type SearchArticlesResponseData = SearchArticlesResponse;
type UseSearchArticlesOptions = Omit<
  UseInfiniteQueryOptions<
    SearchArticlesResponseData,
    ReactQueryError,
    InfiniteData<SearchArticlesResponseData, number>,
    SearchArticlesResponseData,
    QueryKey,
    number
  >,
  | "queryKey"
  | "queryFn"
  | "initialPageParam"
  | "getNextPageParam"
  | "getPreviousPageParam"
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
  inView?: boolean,
  options?: UseSearchArticlesOptions,
) => {
  const q = useInfiniteQuery<
    SearchArticlesResponseData,
    ReactQueryError,
    InfiniteData<SearchArticlesResponseData, number>,
    QueryKey,
    number
  >({
    queryKey: ["articles", query],
    queryFn: ({ pageParam }) =>
      searchArticles({ ...query, page_index: pageParam }),
    initialPageParam: 0,
    getNextPageParam: (lastPage, allPages, lastPageParam) => {
      if (!lastPage.articles_has_next_page) {
        return undefined;
      }
      return lastPageParam + 1;
    },
    getPreviousPageParam: (firstPage, allPages, firstPageParam) => {
      if (firstPageParam <= 0) {
        return undefined;
      }
      return firstPageParam - 1;
    },
    ...options,
  });

  const { fetchNextPage } = q;

  useEffect(() => {
    if (inView) {
      fetchNextPage();
    }
  }, [inView, fetchNextPage]);

  return q;
};
