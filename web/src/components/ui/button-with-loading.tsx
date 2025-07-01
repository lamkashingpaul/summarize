"use client";

import { Button, ButtonProps } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

interface ButtonWithLoadingProps extends ButtonProps {
  isLoading: boolean;
}

export const ButtonWithLoading = (props: ButtonWithLoadingProps) => {
  const { isLoading, children, disabled, ...rest } = props;

  return (
    <Button disabled={isLoading || disabled} {...rest}>
      {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
      {children}
    </Button>
  );
};
