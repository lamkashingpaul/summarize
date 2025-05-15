type ArticlePageProps = {
  params: Promise<{ articleId: string }>;
};

export default async function ArticlePage(props: ArticlePageProps) {
  const { articleId } = await props.params;

  return (
    <div className="container-wrapper">
      <div className="container">
        <h1 className="text-4xl font-bold">Article {articleId}</h1>
        <p>Article content goes here...</p>
      </div>
    </div>
  );
}
