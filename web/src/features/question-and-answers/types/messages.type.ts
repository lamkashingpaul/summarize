type MessageBase = {
  id: string;
  role: "user" | "assistant";
  content: string;
  error?: boolean;
};

export type UserMessage = MessageBase & {
  role: "user";
  relatedAssistantMessageId: string;
  retryable?: boolean;
};

export type AssistantMessage = MessageBase & {
  role: "assistant";
  relatedUserMessageId: string;
  followupQuestions: string[];
  isAssistantMessageLoading?: boolean;
};

export type Message = UserMessage | AssistantMessage;
