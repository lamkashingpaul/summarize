import { SearchArticles } from "@/features/articles/components";

export default function Home() {
  return (
    <section className="my-auto">
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
}
