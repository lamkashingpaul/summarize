import { HydrationSlice } from "@/features/common/types";
import { StateCreator } from "zustand";

export const createHydrationSlice: StateCreator<HydrationSlice> = (set) => ({
  _hasHydrated: false,
  setHasHydrated: (hydrated) => set({ _hasHydrated: hydrated }),
});
