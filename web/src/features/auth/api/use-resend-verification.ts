import { resendVerificationSchema } from "@/features/auth/schemas";
import { ResendVerificationResponse } from "@/features/auth/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/types";
import { useMutation } from "@tanstack/react-query";
import { z } from "zod";

type ResendVerificationDto = z.output<typeof resendVerificationSchema>;

const resendVerification = async (body: ResendVerificationDto) => {
  const response = await customFetch.post<ResendVerificationResponse>(
    "/auth/resend-verification-email",
    body,
  );
  return response.data;
};

const resendVerificationMutationKey = [
  "auth",
  "resend-verification-email",
] as const;

export const useResendVerification = () => {
  const mutation = useMutation<
    ResendVerificationResponse,
    ReactQueryError,
    ResendVerificationDto
  >({
    mutationKey: resendVerificationMutationKey,
    mutationFn: resendVerification,
  });

  return mutation;
};
