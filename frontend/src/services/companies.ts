import api from '../lib/api';
import type { Company } from '../types';

export const companiesService = {
  getAll: async (params?: { page?: number; page_size?: number; industry?: string }) => {
    const response = await api.get('/companies', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/companies/${id}`);
    return response.data;
  },

  create: async (data: Partial<Company>) => {
    const response = await api.post('/companies', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Company>) => {
    const response = await api.put(`/companies/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    await api.delete(`/companies/${id}`);
  },
};
