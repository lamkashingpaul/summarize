import {
  Alert,
  AlertDescription,
  AlertProps,
  AlertTitle,
} from "@/components/ui/alert";
import { cn } from "@/lib/utils";
import { XCircleIcon } from "lucide-react";

type AlertFailureProps = Omit<AlertProps, "title"> & {
  icon?: React.ReactNode | null;
  title?: string | null;
  description?: string | null;
};

export const AlertFailure = (props: AlertFailureProps) => {
  const {
    icon = <XCircleIcon />,
    title = "Failure",
    description = "An error occurred.",
    className,
    ...rest
  } = props;

  return (
    <Alert
      className={cn("bg-red-50 text-red-500", className)}
      variant="default"
      {...rest}
    >
      {icon !== null ? icon : null}
      {title !== null ? <AlertTitle>{title}</AlertTitle> : null}
      {description !== null ? (
        <AlertDescription>{description}</AlertDescription>
      ) : null}
    </Alert>
  );
};
