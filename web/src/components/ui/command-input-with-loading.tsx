"use client";

import { cn } from "@/lib/utils";
import { Command as CommandPrimitive } from "cmdk";
import { Loader2, SearchIcon } from "lucide-react";

type CommandInputWithLoadingProps = React.ComponentProps<
  typeof CommandPrimitive.Input
> & {
  isLoading?: boolean;
};

function CommandInputWithLoading({
  className,
  isLoading,
  ...props
}: CommandInputWithLoadingProps) {
  return (
    <div
      data-slot="command-input-wrapper"
      className="flex h-9 items-center gap-2 border-b px-3"
    >
      <SearchIcon className="size-4 shrink-0 opacity-50" />
      <CommandPrimitive.Input
        data-slot="command-input"
        className={cn(
          "placeholder:text-muted-foreground flex h-10 w-full rounded-md bg-transparent py-3 text-sm outline-hidden disabled:cursor-not-allowed disabled:opacity-50",
          className,
        )}
        {...props}
      />
      {isLoading ? <Loader2 className="text-primary/50 animate-spin" /> : null}
    </div>
  );
}

export { CommandInputWithLoading };
