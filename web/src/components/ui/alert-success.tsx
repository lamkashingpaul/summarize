import {
  Alert,
  AlertDescription,
  AlertProps,
  AlertTitle,
} from "@/components/ui/alert";
import { cn } from "@/lib/utils";
import { CheckCircle2Icon } from "lucide-react";

type AlertSuccessProps = AlertProps & {
  icon?: React.ReactNode;
  title?: string;
  description?: string;
};

export const AlertSuccess = (props: AlertSuccessProps) => {
  const { icon, title, description, className, ...rest } = props;

  const alertIcon = icon || <CheckCircle2Icon />;
  const alertTitle = title || "Success";

  return (
    <Alert
      className={cn("bg-green-50 text-green-500", className)}
      variant="default"
      {...rest}
    >
      {alertIcon}
      <AlertTitle>{alertTitle}</AlertTitle>
      {description && <AlertDescription>{description}</AlertDescription>}
    </Alert>
  );
};
