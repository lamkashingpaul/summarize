import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { FeatureDetails, FeatureStatus } from "@/types";

type FeatureCardProps = {
  card: FeatureDetails;
};

export const FeatureCard = (props: FeatureCardProps) => {
  const { title, description, icon, status, eta } = props.card;
  return (
    <Card className="h-full overflow-hidden transition-all hover:shadow-md">
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between">
          <div className="bg-primary/10 text-primary flex h-10 w-10 items-center justify-center rounded-full">
            {icon}
          </div>
          <StatusBadge status={status} />
        </div>
        <CardTitle className="mt-4">{title}</CardTitle>
        {eta && <CardDescription>Expected: {eta}</CardDescription>}
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground">{description}</p>
      </CardContent>
    </Card>
  );
};

const StatusBadge = ({ status }: { status: FeatureStatus }) => {
  if (status === "planned") {
    return <Badge variant="outline">Planned</Badge>;
  }

  if (status === "in-progress") {
    return (
      <Badge className="bg-amber-500 hover:bg-amber-600">In Progress</Badge>
    );
  }

  return <Badge className="bg-green-500 hover:bg-green-600">Completed</Badge>;
};
