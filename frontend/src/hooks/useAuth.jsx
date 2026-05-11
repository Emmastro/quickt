import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { authService } from '../services/auth.service';
import { storage } from '../utils/storage';
import { showToast } from '../utils/toast';
import { t } from '../i18n';

export function useCurrentUser() {
  return useQuery({
    queryKey: ['auth', 'me'],
    queryFn: authService.getMe,
    enabled: !!storage.getAccessToken(),
    retry: false,
  });
}

export function useLogin() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: authService.login,
    onSuccess: (data) => {
      storage.setAccessToken(data.access_token);
      storage.setRefreshToken(data.refresh_token);
      queryClient.invalidateQueries({ queryKey: ['auth', 'me'] });
      showToast.success(t('toast.login_success'));
    },
  });
}

export function useRegister() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: authService.register,
    onSuccess: (data) => {
      storage.setAccessToken(data.access_token);
      storage.setRefreshToken(data.refresh_token);
      queryClient.invalidateQueries({ queryKey: ['auth', 'me'] });
      showToast.success(t('toast.register_success'));
    },
  });
}

export function useUpdatePreferences() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: authService.updatePreferences,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auth', 'me'] });
    },
  });
}

export function useLogout() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {},
    onSuccess: () => {
      storage.clearAuth();
      queryClient.clear();
      window.location.href = '/login';
    },
  });
}
