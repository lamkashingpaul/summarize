export type AskQuestionResponse = {
  answer: string;
  followup_questions: string[];
  is_related: boolean;
};
