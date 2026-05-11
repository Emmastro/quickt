import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { tripsService } from '../services/trips.service';

export function useTrips() {
  return useQuery({
    queryKey: ['trips'],
    queryFn: tripsService.list,
  });
}

export function useCreateTrip() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: tripsService.create,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['trips'] }),
  });
}

export function useDeleteTrip() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: tripsService.delete,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['trips'] }),
  });
}
