import api from '../lib/api';
import type { Product } from '../types';

export const productsService = {
  getAll: async (params?: { page?: number; page_size?: number; type?: string; is_active?: boolean }) => {
    const response = await api.get('/products', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  create: async (data: Partial<Product>) => {
    const response = await api.post('/products', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Product>) => {
    const response = await api.put(`/products/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    await api.delete(`/products/${id}`);
  },
};
