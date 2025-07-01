import { GitHubIcon } from "@/components/github-icon";
import { ComingSoonButton } from "@/components/ui/coming-soon-button";
import { Mail } from "lucide-react";

type SocialSignUpFormProps = {
  disabled?: boolean;
};

export const SocialSignUpForm = (props: SocialSignUpFormProps) => {
  const { disabled } = props;

  return (
    <div className="grid grid-cols-2 gap-4">
      <ComingSoonButton
        variant="outline"
        className="w-full"
        disabled={disabled}
      >
        <Mail className="mr-2 h-4 w-4" />
        Google
      </ComingSoonButton>
      <ComingSoonButton
        variant="outline"
        className="w-full"
        disabled={disabled}
      >
        <GitHubIcon className="mr-2 h-4 w-4" />
        GitHub
      </ComingSoonButton>
    </div>
  );
};
