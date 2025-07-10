import { z } from "zod";

export const getArticleByIdSchema = z.object({
  params: z.object({
    articleId: z.string().min(1, { error: "Article ID is required" }),
  }),
});
