import { SiteLayout } from "@/components/site-layout";
import { ArticlePageHeader } from "@/features/articles/components/article-page-header";

export default function ArticleLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <SiteLayout header={<ArticlePageHeader />}>{children}</SiteLayout>;
}
