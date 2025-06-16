import { ArticleSummarySection } from "@/components/article-summary-section";
import { ArticleChatbotSection } from "@/components/article-chatbot-section";
import { createGetArticleByIdQueryOptions } from "@/features/articles/api/use-get-article-by-id";
import { getQueryClient } from "@/lib/react-query";
import { dehydrate, HydrationBoundary } from "@tanstack/react-query";
import { Metadata } from "next";

type ArticlePageProps = {
  params: Promise<{ articleId: string }>;
};

export async function generateMetadata(
  props: ArticlePageProps,
): Promise<Metadata> {
  const { articleId } = await props.params;
  const queryClient = getQueryClient();

  const { article } = await queryClient.fetchQuery(
    createGetArticleByIdQueryOptions({ articleId }),
  );
  const title = article?.title || `Article ${articleId}`;

  return { title };
}

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
