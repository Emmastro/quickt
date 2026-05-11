import apiClient from '../api/client';

export const paymentsService = {
  initiate: async (data) => {
    const resp = await apiClient.post('/payments/initiate', data);
    return resp.data;
  },
  getStatus: async (id) => {
    const resp = await apiClient.get(`/payments/${id}/status`);
    return resp.data;
  },
  getMyPayments: async () => {
    const resp = await apiClient.get('/payments/my');
    return resp.data;
  },
};
