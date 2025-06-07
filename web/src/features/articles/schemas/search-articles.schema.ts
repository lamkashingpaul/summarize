import { z } from "zod/v4";

export const searchArticlesSchema = z.object({
  query: z.object({
    title: z.string().optional().default(""),
    page_index: z.number().min(0).optional().default(0),
    page_size: z.number().min(1).max(50).optional().default(10),
  }),
});
