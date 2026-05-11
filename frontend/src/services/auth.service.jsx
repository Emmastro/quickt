import apiClient from '../api/client';

export const authService = {
  register: async (data) => {
    const resp = await apiClient.post('/auth/register', data);
    return resp.data;
  },
  login: async (data) => {
    const resp = await apiClient.post('/auth/login', data);
    return resp.data;
  },
  getMe: async () => {
    const resp = await apiClient.get('/auth/me');
    return resp.data;
  },
  updatePreferences: async (data) => {
    const resp = await apiClient.patch('/auth/me', data);
    return resp.data;
  },
  forgotPassword: async (email) => {
    const resp = await apiClient.post('/auth/forgot-password', { email });
    return resp.data;
  },
  resetPassword: async (data) => {
    const resp = await apiClient.post('/auth/reset-password', data);
    return resp.data;
  },
};
