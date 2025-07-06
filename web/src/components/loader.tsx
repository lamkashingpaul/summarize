import { cn } from "@/lib/utils";

type LoaderProps = {
  className?: string;
};

export const Loader = (props: LoaderProps) => {
  const { className } = props;

  return (
    <div
      className={cn(
        "border-primary h-12 w-12 animate-spin rounded-full border-4 border-t-transparent",
        className,
      )}
    />
  );
};
