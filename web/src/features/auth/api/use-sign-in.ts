import { signInSchema } from "@/features/auth/schemas/sign-in.schema";
import { SignInResponse } from "@/features/auth/types";
import { customFetch } from "@/lib/axois";
import { ReactQueryError } from "@/types";
import { useMutation } from "@tanstack/react-query";
import { z } from "zod/v4";

type SignInDto = z.output<typeof signInSchema>;

const signIn = async (body: SignInDto) => {
  const response = await customFetch.post<SignInResponse>("/auth/login", body);
  return response.data;
};

const signInMutationKey = ["auth", "login"] as const;

export const useSignIn = () => {
  const mutation = useMutation<SignInResponse, ReactQueryError, SignInDto>({
    mutationKey: signInMutationKey,
    mutationFn: signIn,
  });

  return mutation;
};
