import apiClient from '../api/client';

export const ticketsService = {
  reserve: async (data) => {
    const resp = await apiClient.post('/tickets/', data);
    return resp.data;
  },
  getMyTickets: async () => {
    const resp = await apiClient.get('/tickets/my');
    return resp.data;
  },
  getById: async (id) => {
    const resp = await apiClient.get(`/tickets/${id}`);
    return resp.data;
  },
  getByCode: async (code) => {
    const resp = await apiClient.get(`/tickets/code/${code}`);
    return resp.data;
  },
  cancel: async (id, reason) => {
    const resp = await apiClient.patch(`/tickets/${id}/cancel`, { reason });
    return resp.data;
  },
  markUsed: async (id) => {
    const resp = await apiClient.patch(`/tickets/${id}/use`);
    return resp.data;
  },
  getDeparturePassengers: async (departureId) => {
    const resp = await apiClient.get(`/tickets/departure/${departureId}/passengers`);
    return resp.data;
  },
};
