import { IntroductionSectionCard } from "@/components/introduction-section-card";
import { SectionHeading } from "@/components/section-heading";
import { IntroDetails } from "@/types";
import { Brain, Database, Info, MessageSquare } from "lucide-react";

export const IntroductionSection = () => {
  return (
    <section className="bg-muted/30 py-12 md:py-24 lg:py-32">
      <div className="container-wrapper">
        <div className="container">
          <SectionHeading
            id="introduction"
            title="About Summarize"
            description="Your AI-powered platform for research paper summarization and comprehension"
            icon={<Info className="size-6" />}
          />

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {introductionSectionCards.map((card) => (
              <IntroductionSectionCard key={card.id} card={card} />
            ))}
          </div>

          <div className="bg-card mt-10 rounded-lg border p-6 shadow-sm">
            <h3 className="mb-4 text-xl font-semibold">Our Mission</h3>
            <div className="space-y-4">
              {ourMissionDetails.map((detail, i) => (
                <p key={i} className="text-muted-foreground">
                  {detail}
                </p>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

const introductionSectionCards: IntroDetails[] = [
  {
    title: "AI-Powered Summaries",
    description: `Our advanced AI models analyze complex research papers and generate concise, accurate summaries that capture the key findings and methodologies.`,
    icon: <Brain className="text-primary size-5" />,
    id: "ai-powered-summaries",
  },
  {
    title: "RAG Technology",
    description: `Retrieval-Augmented Generation ensures that summaries are grounded in the paper's actual content, providing accurate information without hallucinations or misinterpretations.`,
    icon: <Database className="text-primary size-5" />,
    id: "rag-technology",
  },
  {
    title: "Interactive Q&A",
    description: `Ask specific questions about any paper and receive targeted answers drawn directly from the content, helping you understand complex concepts without reading the entire document.`,
    icon: <MessageSquare className="text-primary size-5" />,
    id: "interactive-qa",
  },
];

const ourMissionDetails: string[] = [
  `Summarize was created to democratize access to scientific knowledge. We believe that valuable research insights should be accessible to everyone, regardless of their technical background or time constraints.`,
  `By leveraging cutting-edge AI technology, we transform dense, complex research papers into clear, digestible summaries and interactive experiences. Our platform serves researchers, students, professionals, and curious minds who want to stay informed about the latest developments across various fields without drowning in technical jargon.`,
  `As we grow, we're building a community where members can contribute their expertise, create and share their own summaries, and collaborate to make research more accessible for everyone.`,
];
