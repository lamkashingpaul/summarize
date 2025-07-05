import { emailSchema } from "@/features/auth/schemas/email.schema";
import { z } from "zod/v4";

export const resendVerificationSchema = z.object({
  email: emailSchema,
});
