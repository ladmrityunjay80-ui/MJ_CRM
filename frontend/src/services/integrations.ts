import api from '../lib/api';

export interface Integration {
  id: string;
  name: string;
  provider: string;
  description?: string;
  config?: any;
  api_key?: string;
  webhook_url?: string;
  status: string;
  last_sync_at?: string;
  organization_id: string;
  created_by_id?: string;
  created_at: string;
  updated_at: string;
}

export interface IntegrationLog {
  id: string;
  integration_id: string;
  operation: string;
  status: string;
  records_processed?: any;
  error_message?: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export const integrationsService = {
  getAll: async (params?: { page?: number; page_size?: number; provider?: string; status?: string }) => {
    const response = await api.get('/integrations', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/integrations/${id}`);
    return response.data;
  },

  create: async (data: Partial<Integration>) => {
    const response = await api.post('/integrations', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Integration>) => {
    const response = await api.put(`/integrations/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/integrations/${id}`);
    return response.data;
  },

  sync: async (id: string) => {
    const response = await api.post(`/integrations/${id}/sync`);
    return response.data;
  },

  getAvailableProviders: async () => {
    const response = await api.get('/integrations/providers/available');
    return response.data;
  },

  getLogs: async (integrationId: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get(`/integrations/${integrationId}/logs`, { params });
    return response.data;
  },

  testConnection: async (id: string) => {
    const response = await api.post(`/integrations/${id}/test`);
    return response.data;
  },

  getProviderConfig: async (provider: string) => {
    const response = await api.get(`/integrations/providers/${provider}/config`);
    return response.data;
  },
};
