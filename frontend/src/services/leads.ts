import api from '../lib/api';
import type { Lead } from '../types';

export const leadsService = {
  getAll: async (params?: { page?: number; page_size?: number; status?: string; assigned_to?: string }) => {
    const response = await api.get('/leads', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/leads/${id}`);
    return response.data;
  },

  create: async (data: Partial<Lead>) => {
    const response = await api.post('/leads', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Lead>) => {
    const response = await api.put(`/leads/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    await api.delete(`/leads/${id}`);
  },
};
