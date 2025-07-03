import { forgotPasswordSchema } from "@/features/auth/schemas";
import { sendResetEmailResponse } from "@/features/auth/types";
import { customFetch } from "@/lib/axois";
import { useMutation } from "@tanstack/react-query";
import { z } from "zod/v4";

type ForgotPasswordDto = z.output<typeof forgotPasswordSchema>;

const sendResetEmail = async (body: ForgotPasswordDto) => {
  const response = await customFetch.post<sendResetEmailResponse>(
    "/auth/send-reset-password-email",
    body,
  );
  return response.data;
};

const sendResetEmailMutationKey = ["auth", "send-reset-password-email"];

export const useSendResetEmail = () => {
  const mutation = useMutation({
    mutationKey: sendResetEmailMutationKey,
    mutationFn: sendResetEmail,
  });

  return mutation;
};
