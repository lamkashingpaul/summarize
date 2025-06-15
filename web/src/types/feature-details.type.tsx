import { ReactNode } from "react";

export type FeatureStatus = "planned" | "in-progress" | "completed";

export type FeatureDetails = {
  title: string;
  description: string;
  icon: ReactNode;
  status: FeatureStatus;
  eta: string;
};
