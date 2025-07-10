import { verifyEmailSchema } from "@/features/auth/schemas";
import { VerifyEmailResponse } from "@/features/auth/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/types";
import { useMutation } from "@tanstack/react-query";
import { z } from "zod";

type VerifyEmailDto = z.output<typeof verifyEmailSchema>;

const verifyEmail = async (body: VerifyEmailDto) => {
  const response = await customFetch.post<VerifyEmailResponse>(
    "/auth/verify-email",
    body,
  );
  return response.data;
};

const verifyEmailMutationKey = ["auth", "verify-email"] as const;

export const useVerifyEmail = () => {
  const mutation = useMutation<
    VerifyEmailResponse,
    ReactQueryError,
    VerifyEmailDto
  >({
    mutationKey: verifyEmailMutationKey,
    mutationFn: verifyEmail,
  });

  return mutation;
};
