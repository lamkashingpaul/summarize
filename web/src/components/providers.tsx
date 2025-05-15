import { ReactQueryClientProvider } from "@/components/react-query-client-provider";

export function Providers({ children }: { children: React.ReactNode }) {
  return <ReactQueryClientProvider>{children}</ReactQueryClientProvider>;
}
