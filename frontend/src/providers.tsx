import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactNode, useMemo } from "react";
import { TopProgress } from "./components/TopProgress";
import { ToastContainer } from "./toast/ToastContainer";

export function AppProviders({ children }: { children: ReactNode }) {
  const client = useMemo(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60_000,
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      }),
    [],
  );
  return (
    <QueryClientProvider client={client}>
      <TopProgress />
      {children}
      <ToastContainer />
    </QueryClientProvider>
  );
}
