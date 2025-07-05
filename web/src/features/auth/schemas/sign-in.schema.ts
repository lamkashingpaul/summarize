import { emailSchema } from "@/features/auth/schemas/email.schema";
import { z } from "zod/v4";

export const signInSchema = z
  .object({
    email: emailSchema,
    password: z.string().min(1, "Password is required"),
    rememberMe: z.boolean().optional(),
  })
  .transform((data) => ({
    email: data.email.toLowerCase(),
    password: data.password,
    remember_me: data.rememberMe ?? false,
  }));
