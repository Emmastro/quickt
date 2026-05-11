import apiClient from '../api/client';

export const tripsService = {
  list: async () => {
    const resp = await apiClient.get('/trips/');
    return resp.data;
  },
  create: async (data) => {
    const resp = await apiClient.post('/trips/', data);
    return resp.data;
  },
  update: async (id, data) => {
    const resp = await apiClient.patch(`/trips/${id}`, data);
    return resp.data;
  },
  delete: async (id) => {
    const resp = await apiClient.delete(`/trips/${id}`);
    return resp.data;
  },
};
