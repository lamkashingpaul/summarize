import {
  Alert,
  AlertDescription,
  AlertProps,
  AlertTitle,
} from "@/components/ui/alert";
import { cn } from "@/lib/utils";
import { CheckCircle2Icon } from "lucide-react";

type AlertSuccessProps = Omit<AlertProps, "title"> & {
  icon?: React.ReactNode | null;
  title?: string | null;
  description?: string | null;
};

export const AlertSuccess = (props: AlertSuccessProps) => {
  const {
    icon = <CheckCircle2Icon />,
    title = "Success",
    description = "Operation completed successfully.",
    className,
    ...rest
  } = props;

  return (
    <Alert
      className={cn("bg-green-50 text-green-500", className)}
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
