import { AuthenticatedUser } from "@/features/users/types";

export type SessionSlice = {
  user: AuthenticatedUser | null;
  loginUser: (user: AuthenticatedUser) => void;
  logoutUser: () => void;
};
