import { FeatureCard } from "@/components/feature-card";
import { SectionHeading } from "@/components/section-heading";
import { ComingSoonButton } from "@/components/ui/coming-soon-button";
import { FeatureDetails } from "@/types";
import {
  Edit,
  FileSearch,
  FolderPlus,
  Layers,
  Rocket,
  UserPlus,
  Users,
} from "lucide-react";

export const RoadmapSection = () => {
  return (
    <section className="bg-muted/30 py-12 md:py-24 lg:py-32">
      <div className="container-wrapper">
        <div className="container">
          <SectionHeading
            id="roadmap"
            title="Future Roadmap"
            description="Exciting features we're working on"
            icon={<Rocket className="h-6 w-6" />}
          />

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {roadmapItems.map((item, i) => (
              <FeatureCard key={i} card={item} />
            ))}
          </div>

          <div className="bg-card mt-10 rounded-lg border p-6 shadow-sm">
            <h3 className="mb-4 text-xl font-semibold">
              Community Contributions
            </h3>
            <div className="space-y-2">
              {communityContributions.map((contribution, i) => (
                <p key={i} className="text-muted-foreground">
                  {contribution}
                </p>
              ))}
              <ComingSoonButton className="gap-2">
                <Rocket className="h-4 w-4" />
                Submit Feature Request
              </ComingSoonButton>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

const roadmapItems: FeatureDetails[] = [
  {
    title: "Member System",
    description: `Create your account to save favorite papers, track reading history, and personalize your experience.`,
    icon: <UserPlus className="h-5 w-5" />,
    status: "in-progress",
    eta: "July 2025",
  },
  {
    title: "Content Management",
    description: `Members will be able to create, edit, and manage their own summaries and annotations of research papers.`,
    icon: <Edit className="h-5 w-5" />,
    status: "in-progress",
    eta: "July 2025",
  },
  {
    title: "Personal Collections",
    description: `Organize papers into custom collections and share them with colleagues or the community.`,
    icon: <FolderPlus className="h-5 w-5" />,
    status: "planned",
    eta: "August 2025",
  },
  {
    title: "Citation Management",
    description: `Export citations in various formats and create bibliographies from your saved papers.`,
    icon: <FileSearch className="h-5 w-5" />,
    status: "planned",
    eta: "August 2025",
  },
  {
    title: "Collaborative Workspaces",
    description: `Create shared spaces where teams can collaborate on research papers with shared notes and summaries.`,
    icon: <Users className="h-5 w-5" />,
    status: "planned",
    eta: "September 2025",
  },
  {
    title: "Knowledge Graphs",
    description: `Visualize connections between papers, authors, and concepts to discover related research.`,
    icon: <Layers className="h-5 w-5" />,
    status: "planned",
    eta: "October 2025",
  },
];

const communityContributions: string[] = [
  `We're building Summarize as a platform where members can contribute their expertise. Soon, you'll be able to create your own summaries, add annotations to existing content, and share your insights with the community.`,
  `Our vision is to create a collaborative ecosystem where AI and human intelligence work together to make research more accessible and understandable for everyone.`,
];
