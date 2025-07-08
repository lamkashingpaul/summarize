import { SessionSlice } from "@/features/auth/types";
import { StateCreator } from "zustand";

export const createSessionSlice: StateCreator<SessionSlice> = (set) => ({
  user: null,
  loginUser: (user) => set({ user }),
  logoutUser: () => set({ user: null }),
});
