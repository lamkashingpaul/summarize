import { passwordSchema } from "@/features/auth/schemas/password.schema";
import { z } from "zod/v4";

export const signUpSchema = z
  .object({
    name: z
      .string()
      .trim()
      .min(1, "Name is required")
      .max(255, "Name must be at most 255 characters long"),
    email: z
      .email({
        error: (issue) => {
          if (!issue.input) {
            return "Email is required";
          }
          return "Invalid email address";
        },
      })
      .min(1, "Email is required"),
    password: passwordSchema,
    confirmPassword: passwordSchema,
    agreedToTerms: z.boolean(),
    subscribeToNewsletter: z.boolean(),
  })
  .check((ctx) => {
    const { password, confirmPassword, agreedToTerms } = ctx.value;
    if (password !== confirmPassword) {
      ctx.issues.push({
        code: "custom",
        message: "Passwords do not match",
        input: ctx.value.confirmPassword,
        path: ["confirmPassword"],
      });
    }

    if (!agreedToTerms) {
      ctx.issues.push({
        code: "custom",
        message: "You must agree to the terms and conditions",
        input: ctx.value.agreedToTerms,
        path: ["agreedToTerms"],
      });
    }
  });
