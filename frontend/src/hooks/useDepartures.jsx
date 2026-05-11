import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { departuresService } from '../services/departures.service';

export function useSearchDepartures(params) {
  return useQuery({
    queryKey: ['departures', 'search', params],
    queryFn: () => departuresService.search(params),
    enabled: !!(params?.origin && params?.destination && params?.date),
  });
}

export function useDepartureDetail(id) {
  return useQuery({
    queryKey: ['departures', 'detail', id],
    queryFn: () => departuresService.getDetail(id),
    enabled: !!id,
  });
}

export function useAgencyDepartures() {
  return useQuery({
    queryKey: ['departures', 'agency'],
    queryFn: departuresService.listByAgency,
  });
}

export function useUpdateDepartureStatus() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }) => departuresService.updateStatus(id, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['departures'] });
    },
  });
}
