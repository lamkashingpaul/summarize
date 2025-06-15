import MarkdownContent from "@/components/markdown-content";
import { Avatar } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { AssistantMessage } from "@/features/question-and-answers/types";
import { cn } from "@/lib/utils";
import { AlertCircle, Bot } from "lucide-react";

type ChatAssistantResponseProps = {
  handleFollowupClick: (question: string) => void;
  status: "error" | "idle" | "pending" | "success";
  message: AssistantMessage;
};

export const ChatAssistantResponse = (props: ChatAssistantResponseProps) => {
  const {
    handleFollowupClick,
    status,
    message: { isAssistantMessageLoading, error, content, followupQuestions },
  } = props;

  if (isAssistantMessageLoading) {
    return <PendingChatAssistantResponse />;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-start gap-3">
        <Avatar className={cn("bg-muted h-8 w-8", error && "bg-destructive")}>
          <div className="flex h-full w-full items-center justify-center">
            {error ? (
              <AlertCircle className="text-destructive-foreground h-4 w-4" />
            ) : (
              <Bot className="h-4 w-4" />
            )}
          </div>
        </Avatar>
        <div className="flex max-w-[80%] flex-col gap-2">
          <div
            className={cn(
              "bg-muted rounded-lg px-4 py-2",
              error && "bg-destructive/10 border-destructive/20 border",
            )}
          >
            <MarkdownContent content={content} />
          </div>
        </div>
      </div>

      {!error && followupQuestions && (
        <div className="ml-11 flex flex-wrap gap-2">
          {followupQuestions.map((question, i) => (
            <Button
              key={i}
              variant="outline"
              size="sm"
              className="text-muted-foreground hover:text-foreground text-xs"
              onClick={() => handleFollowupClick(question)}
              disabled={status === "pending"}
            >
              {question}
            </Button>
          ))}
        </div>
      )}
    </div>
  );
};

const PendingChatAssistantResponse = () => {
  return (
    <div className="flex items-start gap-3">
      <Avatar className="bg-muted h-8 w-8">
        <div className="flex h-full w-full items-center justify-center">
          <Bot className="h-4 w-4" />
        </div>
      </Avatar>
      <div className="bg-muted flex items-center space-x-2 rounded-lg px-4 py-3">
        <div className="bg-muted-foreground h-2 w-2 animate-bounce rounded-full"></div>
        <div
          className="bg-muted-foreground h-2 w-2 animate-bounce rounded-full"
          style={{ animationDelay: "0.2s" }}
        ></div>
        <div
          className="bg-muted-foreground h-2 w-2 animate-bounce rounded-full"
          style={{ animationDelay: "0.4s" }}
        ></div>
      </div>
    </div>
  );
};
