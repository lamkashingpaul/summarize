import { emailSchema } from "@/features/auth/schemas/email.schema";
import { z } from "zod";

export const resendVerificationSchema = z.object({
  email: emailSchema,
});
