import { z } from "zod/v4";

export const getArticleByIdSchema = z.object({
  params: z.object({
    articleId: z.string().min(1, { error: "Article ID is required" }),
  }),
});
