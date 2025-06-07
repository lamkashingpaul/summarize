"use client";

import { useGetArticleByIdSuspense } from "@/features/articles/api/use-get-article-by-id";
import { ArticleSummaryCard } from "@/features/articles/components/article-summary-card";

type ArticleSummarySectionProps = {
  articleId: string;
};

export const ArticleSummarySection = (props: ArticleSummarySectionProps) => {
  const { articleId } = props;
  const { data } = useGetArticleByIdSuspense({ articleId });

  return (
    <section className="y-2 md:py-4 lg:py-6">
      <div className="container-wrapper !max-w-4xl">
        <div className="container">
          <ArticleSummaryCard article={data.article} />
        </div>
      </div>
    </section>
  );
};
