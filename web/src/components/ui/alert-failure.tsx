import {
  Alert,
  AlertDescription,
  AlertProps,
  AlertTitle,
} from "@/components/ui/alert";
import { cn } from "@/lib/utils";
import { XCircleIcon } from "lucide-react";

type AlertFailureProps = AlertProps & {
  icon?: React.ReactNode;
  title?: string;
  description?: string;
};

export const AlertFailure = (props: AlertFailureProps) => {
  const { icon, title, description, className, ...rest } = props;

  const alertIcon = icon || <XCircleIcon />;
  const alertTitle = title || "Failure";

  return (
    <Alert
      className={cn("bg-red-50 text-red-500", className)}
      variant="default"
      {...rest}
    >
      {alertIcon}
      <AlertTitle>{alertTitle}</AlertTitle>
      {description && <AlertDescription>{description}</AlertDescription>}
    </Alert>
  );
};
