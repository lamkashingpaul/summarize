import { z } from "zod/v4";

export const askQuestionSchema = z.object({
  params: z.object({
    articleId: z
      .string()
      .min(1, { error: "Article ID is required" })
      .max(255, { error: "Article ID must be less than 255 characters" }),
  }),
  body: z.object({
    question: z
      .string()
      .min(1, { error: "Question is required" })
      .max(255, { error: "Question must be less than 255 characters" }),
  }),
});
