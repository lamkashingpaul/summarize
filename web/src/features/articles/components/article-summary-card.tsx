import { PlaceholderImage } from "@/components/placeholder-image";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ComingSoonButton } from "@/components/ui/coming-soon-button";
import { ArticleResponse } from "@/features/articles/types";
import { customDayjs } from "@/lib/dayjs";
import { Edit, FileText } from "lucide-react";
import Link from "next/link";

type ArticleSummaryCardProps = {
  article: ArticleResponse;
};

export const ArticleSummaryCard = (props: ArticleSummaryCardProps) => {
  const { article } = props;
  const { title, url, created_at: createAt } = article;

  return (
    <Card className="overflow-hidden p-0">
      <PlaceholderImage title={title} />

      <div className="p-6">
        <div className="text-muted-foreground flex items-center gap-2 text-sm">
          {`Created at: ${customDayjs(createAt).format("LL")}`}
        </div>

        <h1 className="mt-2 text-2xl font-bold md:text-3xl">{title}</h1>

        <div className="mt-6 flex gap-3">
          <Button variant="outline" className="gap-2" asChild>
            <Link href={url} target="_blank" rel="noopener noreferrer">
              <FileText className="h-4 w-4" />
              Read Original Paper
            </Link>
          </Button>
          <ComingSoonButton className="gap-2">
            <Edit className="h-4 w-4" />
            Edit Summary
          </ComingSoonButton>
        </div>
      </div>
    </Card>
  );
};
