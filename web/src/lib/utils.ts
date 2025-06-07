import axios, { AxiosError } from "axios";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { z } from "zod/v4";

type PossibleZodErrorResponse = {
  name?: string;
  issues?: z.core.$ZodIssue[];
};

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const extractFirstZodErrorMessage = (
  error: AxiosError<PossibleZodErrorResponse>,
) => {
  const errorName = error.response?.data?.name;
  if (errorName !== z.core.$ZodError.name || !error.response?.data?.issues) {
    return undefined;
  }

  const issues = error.response.data.issues;
  return issues[0].message;
};

export const formatErrorMessage = (error: unknown) => {
  let message = "Something went wrong, please try again later.";
  if (error instanceof Error && error.message) {
    message = error.message;
  }
  if (axios.isAxiosError(error)) {
    message = error.response?.data?.message || message;
    message = extractFirstZodErrorMessage(error) || message;
  }
  return message;
};
