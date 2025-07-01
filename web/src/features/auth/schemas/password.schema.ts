import { z } from "zod/v4";

export const passwordSchema = z
  .string()
  .min(8, "Password must be at least 8 characters long")
  .max(128, "Password must not exceed 128 characters")
  .refine((val) => /[A-Za-z]/.test(val), {
    error: "Password must contain at least one letter",
  })
  .refine((val) => /[A-Z]/.test(val), {
    error: "Password must contain at least one uppercase letter",
  })
  .refine((val) => /[a-z]/.test(val), {
    error: "Password must contain at least one lowercase letter",
  })
  .refine((val) => /\d/.test(val), {
    error: "Password must contain at least one digit",
  })
  .refine((val) => /[!@#$%^&*()\-_=+[\]{}|;:,.<>/?]/.test(val), {
    error: "Password must contain at least one special character",
  });
