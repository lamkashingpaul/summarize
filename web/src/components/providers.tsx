import { ReactQueryClientProvider } from "@/components/react-query-client-provider";
import { ThemeProvider } from "@/components/theme-provider";
import { NuqsAdapter } from "nuqs/adapters/next/app";
import { Toaster } from "@/components/ui/sonner";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <ReactQueryClientProvider>
        <NuqsAdapter>
          {children}
          <Toaster richColors />
        </NuqsAdapter>
      </ReactQueryClientProvider>
    </ThemeProvider>
  );
}
