import { ChangelogSection } from "@/components/changelog-section";
import { IntroductionSection } from "@/components/introduction-section";
import { RoadmapSection } from "@/components/roadmap-section";
import { SearchArticlesSection } from "@/components/search-articles-section";

export default function Home() {
  return (
    <div className="relative">
      <SearchArticlesSection />
      <IntroductionSection />
      <RoadmapSection />
      <ChangelogSection />
    </div>
  );
}
