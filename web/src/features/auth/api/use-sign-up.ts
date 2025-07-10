import { signUpSchema } from "@/features/auth/schemas/sign-up.schema";
import { SignUpResponse } from "@/features/auth/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/types";
import { useMutation } from "@tanstack/react-query";
import { z } from "zod";

type SignUpDto = z.output<typeof signUpSchema>;

const signUp = async (body: SignUpDto) => {
  const response = await customFetch.post<SignUpResponse>(
    "/auth/register",
    body,
  );
  return response.data;
};

const signUpMutationKey = ["auth", "register"] as const;

export const useSignUp = () => {
  const mutation = useMutation<SignUpResponse, ReactQueryError, SignUpDto>({
    mutationKey: signUpMutationKey,
    mutationFn: signUp,
  });

  return mutation;
};
