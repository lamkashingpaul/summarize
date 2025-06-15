import { ReactNode } from "react";

type SectionHeadingProps = {
  title: string;
  description?: string;
  icon?: ReactNode;
  id?: string;
};

export const SectionHeading = (props: SectionHeadingProps) => {
  const { title, description, icon, id } = props;

  return (
    <div className="mb-8" id={id}>
      <div className="flex items-center gap-2">
        {icon && <div className="text-primary">{icon}</div>}
        <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
      </div>
      {description && (
        <p className="text-muted-foreground mt-1">{description}</p>
      )}
    </div>
  );
};
