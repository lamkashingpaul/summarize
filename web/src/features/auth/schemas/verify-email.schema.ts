import { z } from "zod/v4";

export const verifyEmailSchema = z.object({
  token: z.string(),
});
