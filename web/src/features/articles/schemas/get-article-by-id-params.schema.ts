import { z } from "zod";

export const getArticleByIdParamsSchema = z.object({
  articleId: z.string().min(1, { message: "Article ID is required" }),
});
