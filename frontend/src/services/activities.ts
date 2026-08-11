import api from '../lib/api';
import type { Activity } from '../types';

export const activitiesService = {
  getAll: async (params?: { page?: number; page_size?: number; type?: string; status?: string; deal_id?: string; contact_id?: string }) => {
    const response = await api.get('/activities', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/activities/${id}`);
    return response.data;
  },

  create: async (data: Partial<Activity>) => {
    const response = await api.post('/activities', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Activity>) => {
    const response = await api.put(`/activities/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    await api.delete(`/activities/${id}`);
  },
};
