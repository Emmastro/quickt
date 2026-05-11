import apiClient from '../api/client';

export const notificationsService = {
  list: async () => {
    const resp = await apiClient.get('/notifications/');
    return resp.data;
  },
  markAllRead: async () => {
    await apiClient.post('/notifications/read-all');
  },
  markRead: async (id) => {
    await apiClient.post(`/notifications/${id}/read`);
  },
};
