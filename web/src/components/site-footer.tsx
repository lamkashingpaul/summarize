import {
  authorsLinkedIn,
  projectAuthor,
  projectGithub,
} from "@/lib/site-config";
import { ScrollToTopButton } from "@/components/scroll-to-top-button";

export const SiteFooter = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t py-6 md:py-0">
      <div className="container-wrapper">
        <div className="container py-4">
          <div className="flex flex-col items-center lg:flex-row-reverse lg:justify-between">
            <ScrollToTopButton />

            <div className="text-muted-foreground text-center text-sm leading-loose text-balance md:text-left">
              {`© ${currentYear} `}
              <a
                href={authorsLinkedIn}
                target="_blank"
                rel="noreferrer"
                className="hover:text-primary font-medium underline underline-offset-4 transition-colors"
              >
                {` ${projectAuthor} `}
              </a>
              {"All rights reserved. The source code is available on "}
              <a
                href={`${projectGithub}`}
                target="_blank"
                rel="noreferrer"
                className="hover:text-primary font-medium underline underline-offset-4 transition-colors"
              >
                GitHub
              </a>
              .
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};
