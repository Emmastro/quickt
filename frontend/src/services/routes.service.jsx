import apiClient from '../api/client';

export const routesService = {
  list: async (params) => {
    const resp = await apiClient.get('/routes/', { params });
    return resp.data;
  },
  getById: async (id) => {
    const resp = await apiClient.get(`/routes/${id}`);
    return resp.data;
  },
  getPopular: async (limit = 10) => {
    const resp = await apiClient.get('/routes/popular', { params: { limit } });
    return resp.data;
  },
  create: async (data) => {
    const resp = await apiClient.post('/routes/', data);
    return resp.data;
  },
  update: async (id, data) => {
    const resp = await apiClient.patch(`/routes/${id}`, data);
    return resp.data;
  },
};
