import apiClient from '../api/client';

export const agenciesService = {
  list: async (params) => {
    const resp = await apiClient.get('/agencies/', { params });
    return resp.data;
  },
  getById: async (id) => {
    const resp = await apiClient.get(`/agencies/${id}`);
    return resp.data;
  },
  create: async (data) => {
    const resp = await apiClient.post('/agencies/', data);
    return resp.data;
  },
  update: async (id, data) => {
    const resp = await apiClient.patch(`/agencies/${id}`, data);
    return resp.data;
  },
  approve: async (id) => {
    const resp = await apiClient.patch(`/agencies/${id}/approve`);
    return resp.data;
  },
  suspend: async (id) => {
    const resp = await apiClient.patch(`/agencies/${id}/suspend`);
    return resp.data;
  },
};
