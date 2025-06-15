import { ChangeLogItem } from "@/components/change-log-item";
import { SectionHeading } from "@/components/section-heading";
import { ComingSoonButton } from "@/components/ui/coming-soon-button";
import { ChangeLogDetails } from "@/types";
import { History } from "lucide-react";

export const ChangelogSection = () => {
  return (
    <section className="py-12 md:py-24 lg:py-32">
      <div className="container-wrapper">
        <div className="container">
          <SectionHeading
            id="changelog"
            title="Changelog"
            description="Track our progress and recent updates"
            icon={<History className="size-6" />}
          />

          <div className="space-y-2">
            {changeLogItems.map((item, i) => (
              <ChangeLogItem key={i} item={{ ...item, isLatest: !i }} />
            ))}
          </div>

          <div className="mt-8 text-center">
            <ComingSoonButton variant="outline" className="gap-2">
              <History className="size-4" />
              View Full Changelog
            </ComingSoonButton>
          </div>
        </div>
      </div>
    </section>
  );
};

const changeLogItems: ChangeLogDetails[] = [
  {
    id: "5",
    title: "Missions and Roadmap",
    description: `Introduced missions and roadmap to guide users through the platform's features and future plans.`,
    type: "documentation",
    version: "1.4.0",
    date: "2025-06-15",
  },
  {
    id: "4",
    title: "Interactive Q&A System",
    description: `Added an interactive Q&A system for users to ask questions about papers.`,
    type: "feature",
    version: "1.3.0",
    date: "2025-06-08",
  },
  {
    id: "3",
    title: "RAG Implementation",
    description: `Implemented Retrieval-Augmented Generation (RAG) for enhanced search capabilities.`,
    type: "improvement",
    version: "1.2.0",
    date: "2025-06-01",
  },
  {
    id: "2",
    title: "Paper Detail Pages",
    description: `Introduced detailed pages for each paper with metadata.`,
    type: "feature",
    version: "1.1.0",
    date: "2025-05-25",
  },
  {
    id: "1",
    title: "Initial Release",
    description: `Launched the first version of Summarize with core features.`,
    type: "feature",
    version: "1.0.0",
    date: "2025-05-18",
  },
];
