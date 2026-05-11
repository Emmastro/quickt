import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { showToast } from '../utils/toast';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      retry: 1,
    },
    mutations: {
      onError: (error) => {
        const message = error.response?.data?.detail || error.message || 'Une erreur est survenue';
        showToast.error(message);
      },
    },
  },
});

export default function QueryProvider({ children }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
