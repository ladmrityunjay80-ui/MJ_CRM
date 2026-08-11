import api from '../lib/api';
import type { Deal } from '../types';

export const dealsService = {
  getAll: async (params?: { page?: number; page_size?: number; stage?: string; assigned_to?: string; company_id?: string }) => {
    const response = await api.get('/deals', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/deals/${id}`);
    return response.data;
  },

  create: async (data: Partial<Deal>) => {
    const response = await api.post('/deals', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Deal>) => {
    const response = await api.put(`/deals/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    await api.delete(`/deals/${id}`);
  },
};
