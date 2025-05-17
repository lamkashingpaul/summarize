import { ArticleResponse } from "@/features/articles/types/article-response.type";

export type SearchArticlesResponse = {
  articles_total_count: number;
  articles_total_pages: number;
  articles_has_next_page: boolean;
  articles: ArticleResponse[];
};
