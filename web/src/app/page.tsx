import { ChangelogSection } from "@/components/changelog-section";
import { IntroductionSection } from "@/components/introduction-section";
import { RoadmapSection } from "@/components/roadmap-section";
import { SearchArticlesSection } from "@/components/search-articles-section";
import { SiteLayout } from "@/components/site-layout";

export default function Home() {
  return (
    <SiteLayout>
      <div className="relative">
        <SearchArticlesSection />
        <IntroductionSection />
        <ChangelogSection />
        <RoadmapSection />
      </div>
    </SiteLayout>
  );
}
