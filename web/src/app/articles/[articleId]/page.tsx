import { ArticleSummarySection } from "@/components/article-summary-section";
import { ArticleChatbotSection } from "@/components/article-chatbot-section";
import { createGetArticleByIdQueryOptions } from "@/features/articles/api/use-get-article-by-id";
import { getQueryClient } from "@/lib/react-query";
import { dehydrate, HydrationBoundary } from "@tanstack/react-query";

type ArticlePageProps = {
  params: Promise<{ articleId: string }>;
};

export default async function ArticlePage(props: ArticlePageProps) {
  const { articleId } = await props.params;
  const queryClient = getQueryClient();

  void queryClient.prefetchQuery(
    createGetArticleByIdQueryOptions({ articleId }),
  );

  return (
    <div className="relative">
      <HydrationBoundary state={dehydrate(queryClient)}>
        <ArticleSummarySection articleId={articleId} />
        <ArticleChatbotSection articleId={articleId} />
      </HydrationBoundary>
    </div>
  );
}
