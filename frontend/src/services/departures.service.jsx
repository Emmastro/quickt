import apiClient from '../api/client';

export const departuresService = {
  search: async ({ origin, destination, date }) => {
    const resp = await apiClient.get('/departures/search', {
      params: { origin, destination, date },
    });
    return resp.data;
  },
  getDetail: async (id) => {
    const resp = await apiClient.get(`/departures/detail/${id}`);
    return resp.data;
  },
  listByAgency: async () => {
    const resp = await apiClient.get('/departures/');
    return resp.data;
  },
  updateStatus: async (id, status) => {
    const resp = await apiClient.patch(`/departures/${id}/status`, { status });
    return resp.data;
  },
};
