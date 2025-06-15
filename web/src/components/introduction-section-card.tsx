import { IntroDetails } from "@/types";

type IntroductionSectionCardProps = {
  card: IntroDetails;
};
export const IntroductionSectionCard = (
  props: IntroductionSectionCardProps,
) => {
  const { title, description, icon, id } = props.card;

  return (
    <div id={id} className="bg-card rounded-lg border p-6 shadow-sm">
      <div className="bg-primary/10 mb-4 flex h-10 w-10 items-center justify-center rounded-full">
        {icon}
      </div>
      <h3 className="mb-2 font-semibold">{title}</h3>
      <p className="text-muted-foreground text-sm">{description}</p>
    </div>
  );
};
