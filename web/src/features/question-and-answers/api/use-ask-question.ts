import { askQuestionSchema } from "@/features/question-and-answers/schemas";
import { AskQuestionResponse } from "@/features/question-and-answers/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/types";
import { useMutation, UseMutationOptions } from "@tanstack/react-query";
import { z } from "zod";

type AskQuestionParamsDto = z.infer<typeof askQuestionSchema.shape.params>;
type AskQuestionBodyDto = z.infer<typeof askQuestionSchema.shape.body>;
type UseAskQuestionOptions = Omit<
  UseMutationOptions<AskQuestionResponse, ReactQueryError, AskQuestionBodyDto>,
  "mutationKey" | "mutationFn"
>;

const askQuestion = async (
  articleId: AskQuestionParamsDto["articleId"],
  body: AskQuestionBodyDto,
) => {
  const response = await customFetch.post<AskQuestionResponse>(
    `/question-and-answers/articles/${articleId}/questions`,
    body,
  );
  return response.data;
};

export const useAskQuestion = (
  params: AskQuestionParamsDto,
  options?: UseAskQuestionOptions,
) => {
  const { articleId } = params;

  const mutation = useMutation<
    AskQuestionResponse,
    ReactQueryError,
    AskQuestionBodyDto
  >({
    mutationFn: (body) => askQuestion(articleId, body),
    mutationKey: [
      "question-ans-answers",
      "articles",
      articleId,
      "questions",
    ] as const,
    ...options,
  });

  return mutation;
};
