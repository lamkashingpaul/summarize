import { forgotPasswordSchema } from "@/features/auth/schemas";
import { SendResetEmailResponse } from "@/features/auth/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/types";
import { useMutation } from "@tanstack/react-query";
import { z } from "zod";

type ForgotPasswordDto = z.output<typeof forgotPasswordSchema>;

const sendResetEmail = async (body: ForgotPasswordDto) => {
  const response = await customFetch.post<SendResetEmailResponse>(
    "/auth/send-reset-password-email",
    body,
  );
  return response.data;
};

const sendResetEmailMutationKey = [
  "auth",
  "send-reset-password-email",
] as const;

export const useSendResetEmail = () => {
  const mutation = useMutation<
    SendResetEmailResponse,
    ReactQueryError,
    ForgotPasswordDto
  >({
    mutationKey: sendResetEmailMutationKey,
    mutationFn: sendResetEmail,
  });

  return mutation;
};
