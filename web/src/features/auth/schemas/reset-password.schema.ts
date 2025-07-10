import { passwordSchema } from "@/features/auth/schemas/password.schema";
import { z } from "zod";

export const resetPasswordSchema = z
  .object({
    token: z.string(),
    newPassword: passwordSchema,
    confirmNewPassword: passwordSchema,
  })
  .check((ctx) => {
    const { newPassword, confirmNewPassword } = ctx.value;
    if (newPassword !== confirmNewPassword) {
      ctx.issues.push({
        code: "custom",
        message: "Passwords do not match",
        input: ctx.value.confirmNewPassword,
        path: ["confirmNewPassword"],
      });
    }
  })
  .transform((data) => ({
    token: data.token,
    new_password: data.newPassword,
    confirm_new_password: data.confirmNewPassword,
  }));
