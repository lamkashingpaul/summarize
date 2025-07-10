import { emailSchema } from "@/features/auth/schemas/email.schema";
import { z } from "zod";

export const forgotPasswordSchema = z.object({
  email: emailSchema,
});
