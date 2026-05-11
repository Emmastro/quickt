import { useMutation, useQueryClient } from '@tanstack/react-query';
import { paymentsService } from '../services/payments.service';

export function useInitiatePayment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: paymentsService.initiate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tickets'] });
      queryClient.invalidateQueries({ queryKey: ['departures'] });
    },
  });
}
