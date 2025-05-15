import { getArticleByIdParamsSchema } from "@/features/articles/schemas";
import { GetArticleByIdResponse } from "@/features/articles/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/lib/react-query";
import { useQuery, UseQueryOptions } from "@tanstack/react-query";
import { z } from "zod";

type GetArticleByIdParamsDto = z.infer<typeof getArticleByIdParamsSchema>;
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

export const useGetArticleById = (
  query: GetArticleByIdParamsDto,
  options?: UseGetArticleByIdOptions,
) => {
  const { articleId } = query;
  const q = useQuery<GetArticleByIdResponseData, ReactQueryError>({
    queryKey: ["articles", articleId],
    queryFn: () => getArticleById(articleId),
    ...options,
  });

  return q;
};
