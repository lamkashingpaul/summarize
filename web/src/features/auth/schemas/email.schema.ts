import { z } from "zod";

export const emailSchema = z
  .email({
    error: (issue) => {
      if (!issue.input) {
        return "Email is required";
      }
      return "Invalid email address";
    },
  })
  .transform((value) => value.toLowerCase());
