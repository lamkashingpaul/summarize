import { resetPasswordSchema } from "@/features/auth/schemas";
import { ResetPasswordResponse } from "@/features/auth/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/types";
import { useMutation } from "@tanstack/react-query";
import { z } from "zod";

type ResetPasswordDto = z.output<typeof resetPasswordSchema>;

const resetPassword = async (body: ResetPasswordDto) => {
  const response = await customFetch.post<ResetPasswordResponse>(
    "/auth/reset-password",
    body,
  );
  return response.data;
};

const resetPasswordMutationKey = ["auth", "reset-password"] as const;

export const useResetPassword = () => {
  const mutation = useMutation<
    ResetPasswordResponse,
    ReactQueryError,
    ResetPasswordDto
  >({
    mutationKey: resetPasswordMutationKey,
    mutationFn: resetPassword,
  });

  return mutation;
};
