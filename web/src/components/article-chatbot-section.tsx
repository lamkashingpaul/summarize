"use client";

import { ArticleChatbotCard } from "@/features/question-and-answers/components/article-chatbot-card";
import { useGetArticleByIdSuspense } from "@/features/articles/api/use-get-article-by-id";
import { MessageSquare } from "lucide-react";

type ArticleChatbotSectionProps = {
  articleId: string;
};

export const ArticleChatbotSection = (props: ArticleChatbotSectionProps) => {
  const { articleId } = props;
  const { data } = useGetArticleByIdSuspense({ articleId });
  const { title } = data.article;

  return (
    <section className="y-2 md:py-4 lg:py-6">
      <div className="container-wrapper !max-w-4xl">
        <div className="container">
          <div className="mb-4 flex items-center gap-2">
            <MessageSquare className="h-5 w-5" />
            <h2 className="text-xl font-semibold">Ask about this article</h2>
          </div>

          <ArticleChatbotCard articleId={articleId} articleTitle={title} />
        </div>
      </div>
    </section>
  );
};
