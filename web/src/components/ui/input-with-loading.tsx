import * as React from "react";

import { cn } from "@/lib/utils";
import { Loader2 } from "lucide-react";

export interface InputWithLoadingProps extends React.ComponentProps<"input"> {
  isLoading?: boolean;
  inputClassName?: string;
}

function InputWithLoading({
  className,
  inputClassName,
  type,
  isLoading,
  ...props
}: InputWithLoadingProps) {
  return (
    <div className={cn("relative", className)}>
      <input
        type={type}
        data-slot="input"
        className={cn(
          "file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/30 border-input flex h-9 w-full min-w-0 rounded-md border bg-transparent px-3 py-1 text-base shadow-xs transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
          "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
          "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
          inputClassName,
        )}
        {...props}
      />
      {isLoading ? (
        <div className="absolute top-1/2 right-0 -translate-x-1/2 -translate-y-1/2 transform rounded-full transition-all">
          <Loader2 className="text-primary/50 animate-spin" />
        </div>
      ) : null}
    </div>
  );
}

export { InputWithLoading };
