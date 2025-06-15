import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { ChangeLogDetails, ChangeLogType } from "@/types";

type ChangeLogItemProps = {
  item: ChangeLogDetails;
};

export const ChangeLogItem = (props: ChangeLogItemProps) => {
  const {
    title,
    description,
    type,
    version,
    date,
    isLatest = false,
  } = props.item;

  const { className: itemClassName, icon: itemIcon } = itemTypeToStyles[type];

  return (
    <div className={cn("relative pb-8 pl-8", !isLatest && "ml-4 border-l")}>
      <div
        className={cn(
          "border-background absolute top-0 left-0 flex h-8 w-8 items-center justify-center rounded-full border-4",
          itemClassName,
        )}
      >
        {itemIcon}
      </div>

      <div className="space-y-2">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-muted-foreground text-sm">{date}</span>
          <Badge variant="outline" className="font-mono text-xs">
            v{version}
          </Badge>
          {isLatest && (
            <Badge className="bg-green-500 hover:bg-green-600">Latest</Badge>
          )}
        </div>
        <h3 className="font-semibold">{title}</h3>
        <p className="text-muted-foreground text-sm">{description}</p>
      </div>
    </div>
  );
};

const itemTypeToStyles: Record<
  ChangeLogType,
  { className: string; icon: string }
> = {
  feature: {
    className: "bg-green-100 text-green-600",
    icon: "✦",
  },
  improvement: {
    className: "bg-blue-100 text-blue-600",
    icon: "↑",
  },
  bugfix: {
    className: "bg-amber-100 text-amber-600",
    icon: "✓",
  },
  documentation: {
    className: "bg-purple-100 text-purple-600",
    icon: "★",
  },
  other: {
    className: "bg-gray-100 text-gray-600",
    icon: "•",
  },
};
