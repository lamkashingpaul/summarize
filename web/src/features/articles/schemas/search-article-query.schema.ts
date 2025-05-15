import { z } from "zod";

export const searchArticlesQuerySchema = z.object({
  name: z.string().optional().default(""),
  url: z.string().optional().default(""),
  page_index: z.number().min(0).optional().default(0),
  page_size: z.number().min(1).max(50).optional().default(10),
});
