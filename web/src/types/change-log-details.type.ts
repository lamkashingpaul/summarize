export type ChangeLogType =
  | "feature"
  | "bugfix"
  | "improvement"
  | "documentation"
  | "other";

export type ChangeLogDetails = {
  id?: string;
  title: string;
  description: string;
  type: ChangeLogType;
  version: string;
  date: string;
  isLatest?: boolean;
};
