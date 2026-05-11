import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ticketsService } from '../services/tickets.service';
import { showToast } from '../utils/toast';
import { t } from '../i18n';

export function useReserveTickets() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ticketsService.reserve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['departures'] });
      queryClient.invalidateQueries({ queryKey: ['tickets'] });
    },
  });
}

export function useMyTickets() {
  return useQuery({
    queryKey: ['tickets', 'my'],
    queryFn: ticketsService.getMyTickets,
  });
}

export function useTicketDetail(id) {
  return useQuery({
    queryKey: ['tickets', id],
    queryFn: () => ticketsService.getById(id),
    enabled: !!id,
  });
}

export function useCancelTicket() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, reason }) => ticketsService.cancel(id, reason),
    onSuccess: () => {
      showToast.success(t('toast.ticket_cancelled'));
      queryClient.invalidateQueries({ queryKey: ['tickets'] });
      queryClient.invalidateQueries({ queryKey: ['departures'] });
    },
  });
}

export function useTicketByCode(code) {
  return useQuery({
    queryKey: ['tickets', 'code', code],
    queryFn: () => ticketsService.getByCode(code),
    enabled: !!code,
  });
}
