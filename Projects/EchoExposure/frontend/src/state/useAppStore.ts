import { create } from "zustand";

type Page = "dashboard" | "assets" | "scans" | "surface" | "findings" | "settings";

type AppState = {
  page: Page;
  setPage: (p: Page) => void;
};

export const useAppStore = create<AppState>((set) => ({
  page: "dashboard",
  setPage: (p) => set({ page: p }),
}));
