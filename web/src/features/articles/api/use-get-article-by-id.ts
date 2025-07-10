import { getArticleByIdSchema } from "@/features/articles/schemas";
import { GetArticleByIdResponse } from "@/features/articles/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/types";
import {
  queryOptions,
  useQuery,
  UseQueryOptions,
  useSuspenseQuery,
} from "@tanstack/react-query";
import { z } from "zod";

type GetArticleByIdParamsDto = z.infer<
  typeof getArticleByIdSchema.shape.params
>;
type GetArticleByIdResponseData = GetArticleByIdResponse;
type UseGetArticleByIdOptions = Omit<
  UseQueryOptions<GetArticleByIdResponseData, ReactQueryError>,
  "queryKey" | "queryFn"
>;

const getArticleById = async (
  articleId: GetArticleByIdParamsDto["articleId"],
) => {
  const response = await customFetch<GetArticleByIdResponseData>({
    url: `/articles/${articleId}`,
  });
  return response.data;
};

export const createGetArticleByIdQueryOptions = (
  params: GetArticleByIdParamsDto,
  options?: UseGetArticleByIdOptions,
) => {
  const { articleId } = params;

  return queryOptions<GetArticleByIdResponseData, ReactQueryError>({
    queryFn: () => getArticleById(articleId),
    queryKey: ["articles", articleId],
    ...options,
  });
};

export const useGetArticleById = (
  params: GetArticleByIdParamsDto,
  options?: UseGetArticleByIdOptions,
) => {
  return useQuery(createGetArticleByIdQueryOptions(params, options));
};

export const useGetArticleByIdSuspense = (
  params: GetArticleByIdParamsDto,
  options?: UseGetArticleByIdOptions,
) => {
  return useSuspenseQuery(createGetArticleByIdQueryOptions(params, options));
};
