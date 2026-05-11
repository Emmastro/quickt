import apiClient from '../api/client';

export const busesService = {
  list: async () => {
    const resp = await apiClient.get('/buses/');
    return resp.data;
  },
  getById: async (id) => {
    const resp = await apiClient.get(`/buses/${id}`);
    return resp.data;
  },
  create: async (data) => {
    const resp = await apiClient.post('/buses/', data);
    return resp.data;
  },
  update: async (id, data) => {
    const resp = await apiClient.patch(`/buses/${id}`, data);
    return resp.data;
  },
  delete: async (id) => {
    const resp = await apiClient.delete(`/buses/${id}`);
    return resp.data;
  },
};
