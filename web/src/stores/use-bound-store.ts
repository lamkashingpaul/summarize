import { createSessionSlice } from "@/features/auth/slices/session.slice";
import { SessionSlice } from "@/features/auth/types";
import { create } from "zustand";
import { persist } from "zustand/middleware";

type BoundSlice = SessionSlice;

export const useBoundStore = create<BoundSlice>()(
  persist(
    (...a) => ({
      ...createSessionSlice(...a),
    }),
    {
      name: "session-store",
      partialize: (state) => ({ user: state.user }),
    },
  ),
);
