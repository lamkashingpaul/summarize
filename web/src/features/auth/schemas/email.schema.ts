import { z } from "zod/v4";

export const emailSchema = z
  .email({
    error: (issue) => {
      if (!issue.input) {
        return "Email is required";
      }
      return "Invalid email address";
    },
  })
  .min(1, "Email is required");
