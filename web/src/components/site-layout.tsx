import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { ReactNode } from "react";

type SiteLayoutProps = {
  header?: ReactNode;
  children?: ReactNode;
};

export const SiteLayout = (props: SiteLayoutProps) => {
  const { header = <SiteHeader />, children } = props;

  return (
    <div className="flex min-h-svh flex-col">
      {header}
      <main className="flex flex-1 flex-col">{children}</main>
      <SiteFooter />
    </div>
  );
};
