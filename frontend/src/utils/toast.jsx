import { toast } from 'sonner';

export const showToast = {
  success: (message) => toast.success(message),
  error: (message) => toast.error(message || 'Une erreur est survenue'),
  info: (message) => toast.info(message),
};
