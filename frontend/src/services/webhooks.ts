import api from '../lib/api';

export interface Webhook {
  id: string;
  name: string;
  url: string;
  method: string;
  headers?: Record<string, string>;
  secret?: string;
  events: string[];
  is_active: boolean;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export interface WebhookLog {
  id: string;
  webhook_id: string;
  event_type: string;
  payload: any;
  response_status?: number;
  response_body?: string;
  error_message?: string;
  created_at: string;
}

export const webhooksService = {
  getAll: async (params?: { page?: number; page_size?: number; is_active?: boolean }) => {
    const response = await api.get('/webhooks', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/webhooks/${id}`);
    return response.data;
  },

  create: async (data: Partial<Webhook>) => {
    const response = await api.post('/webhooks', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Webhook>) => {
    const response = await api.put(`/webhooks/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/webhooks/${id}`);
    return response.data;
  },

  test: async (id: string) => {
    const response = await api.post(`/webhooks/${id}/test`);
    return response.data;
  },

  getLogs: async (webhookId: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get(`/webhooks/${webhookId}/logs`, { params });
    return response.data;
  },

  getAvailableEvents: async () => {
    const response = await api.get('/webhooks/events');
    return response.data;
  },
};
