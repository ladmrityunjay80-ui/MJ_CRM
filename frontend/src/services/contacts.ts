import api from '../lib/api';
import type { Contact } from '../types';

export const contactsService = {
  getAll: async (params?: { page?: number; page_size?: number; company_id?: string }) => {
    const response = await api.get('/contacts', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/contacts/${id}`);
    return response.data;
  },

  create: async (data: Partial<Contact>) => {
    const response = await api.post('/contacts', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Contact>) => {
    const response = await api.put(`/contacts/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    await api.delete(`/contacts/${id}`);
  },
};
