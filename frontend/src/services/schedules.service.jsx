import apiClient from '../api/client';

export const schedulesService = {
  list: async () => {
    const resp = await apiClient.get('/schedules/');
    return resp.data;
  },
  getById: async (id) => {
    const resp = await apiClient.get(`/schedules/${id}`);
    return resp.data;
  },
  create: async (data) => {
    const resp = await apiClient.post('/schedules/', data);
    return resp.data;
  },
  update: async (id, data) => {
    const resp = await apiClient.patch(`/schedules/${id}`, data);
    return resp.data;
  },
  generateDepartures: async (id, data) => {
    const resp = await apiClient.post(`/schedules/${id}/generate-departures`, data);
    return resp.data;
  },
};
