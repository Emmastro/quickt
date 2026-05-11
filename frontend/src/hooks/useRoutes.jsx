import { useQuery } from '@tanstack/react-query';
import { routesService } from '../services/routes.service';

export function useRoutes(params) {
  return useQuery({
    queryKey: ['routes', params],
    queryFn: () => routesService.list(params),
  });
}

export function useRoute(id) {
  return useQuery({
    queryKey: ['routes', id],
    queryFn: () => routesService.getById(id),
    enabled: !!id,
  });
}

export function usePopularRoutes(limit = 6) {
  return useQuery({
    queryKey: ['routes', 'popular', limit],
    queryFn: () => routesService.getPopular(limit),
  });
}
