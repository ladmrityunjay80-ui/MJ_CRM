import api from '../lib/api';

export interface Notification {
  id: string;
  title: string;
  message: string;
  notification_type: string;
  is_read: boolean;
  read_at?: string;
  action_url?: string;
  organization_id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export const notificationsService = {
  getAll: async (params?: { page?: number; page_size?: number; is_read?: boolean }) => {
    const response = await api.get('/notifications', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/notifications/${id}`);
    return response.data;
  },

  markAsRead: async (id: string) => {
    const response = await api.patch(`/notifications/${id}/read`);
    return response.data;
  },

  markAllAsRead: async () => {
    const response = await api.patch('/notifications/read-all');
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/notifications/${id}`);
    return response.data;
  },

  getUnreadCount: async () => {
    const response = await api.get('/notifications/unread-count');
    return response.data;
  },

  getPreferences: async () => {
    const response = await api.get('/notifications/preferences');
    return response.data;
  },

  updatePreferences: async (preferences: any) => {
    const response = await api.put('/notifications/preferences', preferences);
    return response.data;
  },
};
