import { SiteLayout } from "@/components/site-layout";

export default function ResendVerificationEmailLayout(
  props: Readonly<{ children: React.ReactNode }>,
) {
  return <SiteLayout header={null}>{props.children}</SiteLayout>;
}
