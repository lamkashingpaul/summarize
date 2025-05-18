import { SearchArticles } from "@/features/articles/components";

export const SearchArticlesSection = () => {
  return (
    <section className="py-12 md:py-24 lg:py-32">
      <div className="container-wrapper">
        <div className="container">
          <div className="flex flex-col items-center justify-center gap-4">
            <h1 className="text-4xl font-bold">
              What can I help you summarize?
            </h1>
            <SearchArticles />
          </div>
        </div>
      </div>
    </section>
  );
};
