import { z } from "zod";

export const createArticleBodySchema = z.object({
  url: z.string().url({ message: "Invalid URL" }),
  name: z.string().min(1, { message: "Name is required" }),
  page_numbers_to_delete: z.array(z.number()).optional().default([]),
});
