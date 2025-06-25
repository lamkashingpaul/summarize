"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { useAskQuestion } from "@/features/question-and-answers/api/use-ask-question";
import { ChatAssistantResponse } from "@/features/question-and-answers/components/chat-assistant-response";
import { ChatUserInput } from "@/features/question-and-answers/components/chat-user-input";
import {
  AssistantMessage,
  Message,
  UserMessage,
} from "@/features/question-and-answers/types";
import { cn, formatErrorMessage } from "@/lib/utils";
import { Bot, Maximize2, Minimize2, SendHorizontal, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";

type ArticleChatbotCardProps = {
  articleId: string;
  articleTitle: string;
};

const welcomeMessage = (articleTitle: string): AssistantMessage => ({
  id: crypto.randomUUID(),
  role: "assistant",
  content: `Welcome to the Q&A bot for the article **"${articleTitle}"**. Ask me anything about this article!`,
  relatedUserMessageId: "",
  followupQuestions: [
    "What are the key findings of this paper?",
    "Can you summarize the methodology?",
    "What are the limitations of this research?",
  ],
  isAssistantMessageLoading: false,
  error: false,
});

export const ArticleChatbotCard = (props: ArticleChatbotCardProps) => {
  const { articleId, articleTitle } = props;
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    welcomeMessage(articleTitle),
  ]);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const { mutateAsync, status } = useAskQuestion({
    articleId,
  });

  const handleUpdateMessages = async (
    question: string,
    userMessageId: string,
    assistantMessageId: string,
  ) => {
    try {
      const { answer, followup_questions: followupQuestions } =
        await mutateAsync({
          question,
        });

      setMessages((oldMessages) =>
        oldMessages.map((message) => {
          if (message.id === userMessageId) {
            return {
              ...message,
              error: false,
              retryable: false,
            };
          }
          if (message.id === assistantMessageId) {
            return {
              ...message,
              content: answer,
              followupQuestions,
              isAssistantMessageLoading: false,
              error: false,
            };
          }
          return message;
        }),
      );
    } catch (error) {
      const errorMessage = formatErrorMessage(error);
      setMessages((oldMessages) =>
        oldMessages.map((message) => {
          if (message.id === userMessageId) {
            return {
              ...message,
              error: true,
              retryable: true,
            };
          }
          if (message.id === assistantMessageId) {
            return {
              ...message,
              content: errorMessage,
              followupQuestions: [],
              error: true,
              isAssistantMessageLoading: false,
            };
          }
          return message;
        }),
      );
    }
  };

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) {
      return;
    }

    const userMessage: UserMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: message,
      relatedAssistantMessageId: "",
      retryable: false,
      error: false,
    };
    const assistantMessage: Message = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "",
      relatedUserMessageId: userMessage.id,
      followupQuestions: [],
      isAssistantMessageLoading: true,
      error: false,
    };
    userMessage.relatedAssistantMessageId = assistantMessage.id;

    setMessages((prev) => [...prev, userMessage, assistantMessage]);
    setInput("");
    await handleUpdateMessages(message, userMessage.id, assistantMessage.id);
  };

  const handleRetry = async (
    messageContent: string,
    retryUserMessageId: string,
    retryAssistantMessageId: string,
  ) => {
    setMessages((oldMessages) =>
      oldMessages.map((message) => {
        if (message.id === retryUserMessageId) {
          return {
            ...message,
            error: false,
            retryable: false,
          };
        }
        if (message.id === retryAssistantMessageId) {
          return {
            ...message,
            isAssistantMessageLoading: true,
            error: false,
          };
        }
        return message;
      }),
    );
    await handleUpdateMessages(
      messageContent,
      retryUserMessageId,
      retryAssistantMessageId,
    );
  };

  const handleFollowupClick = async (question: string) => {
    await handleSendMessage(question);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(input);
    }
  };

  const scrollToView = (behavior: ScrollBehavior) => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  };

  const toggleFullscreen = () => {
    setIsFullscreen((oldIsFullscreen) => !oldIsFullscreen);
  };

  useEffect(() => {
    if (messages.length >= 2) {
      scrollToView("smooth");
    }
  }, [messages]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isFullscreen) {
        setIsFullscreen(false);
      }
    };

    if (isFullscreen) {
      document.addEventListener("keydown", handleEscape);
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
      if (messages.length >= 2) {
        scrollToView("instant");
      }
    }

    return () => {
      document.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = "unset";
    };
  }, [isFullscreen, messages.length]);

  const chatContent = (
    <>
      <div className="flex items-center justify-between border-b p-4">
        <div className="flex items-center gap-2">
          <Bot className="h-5 w-5" />
          <h3 className="font-semibold">AI Research Assistant</h3>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleFullscreen}
            className="h-8 w-8 p-0"
          >
            {isFullscreen ? (
              <Minimize2 className="h-4 w-4" />
            ) : (
              <Maximize2 className="h-4 w-4" />
            )}
            <span className="sr-only">
              {isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}
            </span>
          </Button>
          {isFullscreen && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsFullscreen(false)}
              className="h-8 w-8 p-0"
            >
              <X className="h-4 w-4" />
              <span className="sr-only">Close fullscreen</span>
            </Button>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {messages.map((message) => {
            if (message.role === "user") {
              return (
                <ChatUserInput
                  key={message.id}
                  status={status}
                  message={message}
                  handleRetry={handleRetry}
                />
              );
            }

            if (message.role === "assistant") {
              return (
                <ChatAssistantResponse
                  key={message.id}
                  status={status}
                  message={message}
                  handleFollowupClick={handleFollowupClick}
                />
              );
            }
            return null;
          })}

          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="border-t p-4">
        <div className="flex items-end gap-2">
          <Textarea
            className={cn(
              "resize-none",
              isFullscreen ? "min-h-[80px]" : "min-h-[60px]",
            )}
            placeholder="Ask a question about this article..."
            name="question"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <Button
            className={cn("px-3", isFullscreen ? "h-[80px]" : "h-[60px]")}
            onClick={() => handleSendMessage(input)}
            disabled={status === "pending" || !input.trim()}
          >
            <SendHorizontal className="h-5 w-5" />
            <span className="sr-only">Send message</span>
          </Button>
        </div>
        {isFullscreen && (
          <div className="text-muted-foreground mt-2 text-center text-xs">
            Press{" "}
            <kbd className="bg-muted rounded px-1.5 py-0.5 text-xs">Esc</kbd> to
            exit fullscreen
          </div>
        )}
      </div>
    </>
  );

  if (isFullscreen) {
    return (
      <div className="bg-background fixed inset-0 z-50">
        <div className="flex h-full flex-col">{chatContent}</div>
      </div>
    );
  }

  return (
    <Card className="flex h-[600px] flex-col overflow-hidden py-0">
      {chatContent}
    </Card>
  );
};
