import { Avatar } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { UserMessage } from "@/features/question-and-answers/types";
import { cn } from "@/lib/utils";
import { AlertCircle, RotateCcw, User } from "lucide-react";

type ChatUserInputProps = {
  handleRetry: (
    messageContent: string,
    retryUserMessageId: string,
    retryAssistantMessageId: string,
  ) => void;
  status: "error" | "idle" | "pending" | "success";
  message: UserMessage;
};

export const ChatUserInput = (props: ChatUserInputProps) => {
  const {
    handleRetry,
    status,
    message: {
      error,
      retryable,
      id: userMessageId,
      content,
      relatedAssistantMessageId,
    },
  } = props;

  return (
    <div className="space-y-4">
      <div className="flex flex-row-reverse items-start gap-3">
        <Avatar className={cn("bg-primary h-8 w-8", error && "bg-destructive")}>
          <div className="flex h-full w-full items-center justify-center">
            {error ? (
              <AlertCircle className="text-destructive-foreground h-4 w-4" />
            ) : (
              <User className="text-primary-foreground h-4 w-4" />
            )}
          </div>
        </Avatar>
        <div className="flex max-w-[80%] flex-col gap-2">
          <div className="bg-primary text-primary-foreground rounded-lg px-4 py-2">
            <p className="whitespace-pre-wrap">{content}</p>
          </div>

          {error && retryable ? (
            <div className="flex justify-end">
              <Button
                variant="outline"
                size="sm"
                className="gap-2 text-xs"
                onClick={() =>
                  handleRetry(content, userMessageId, relatedAssistantMessageId)
                }
                disabled={status === "pending"}
              >
                <RotateCcw className="h-3 w-3" />
                Retry
              </Button>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};
