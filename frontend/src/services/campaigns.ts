import api from '../lib/api';

export interface Campaign {
  id: string;
  name: string;
  subject: string;
  body: string;
  status: string;
  scheduled_at?: string;
  sent_at?: string;
  total_recipients: number;
  sent_count: number;
  opened_count: number;
  clicked_count: number;
  organization_id: string;
  created_by_id?: string;
  created_at: string;
  updated_at: string;
}

export interface CampaignRecipient {
  id: string;
  campaign_id: string;
  contact_id: string;
  email: string;
  status: string;
  opened_at?: string;
  clicked_at?: string;
  created_at: string;
  updated_at: string;
}

export const campaignsService = {
  getAll: async (params?: { page?: number; page_size?: number; status?: string }) => {
    const response = await api.get('/campaigns', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/campaigns/${id}`);
    return response.data;
  },

  create: async (data: Partial<Campaign>) => {
    const response = await api.post('/campaigns', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Campaign>) => {
    const response = await api.put(`/campaigns/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/campaigns/${id}`);
    return response.data;
  },

  send: async (id: string) => {
    const response = await api.post(`/campaigns/${id}/send`);
    return response.data;
  },

  schedule: async (id: string, scheduledAt: string) => {
    const response = await api.post(`/campaigns/${id}/schedule`, { scheduled_at: scheduledAt });
    return response.data;
  },

  // Recipients
  getRecipients: async (campaignId: string, params?: { page?: number; page_size?: number; status?: string }) => {
    const response = await api.get(`/campaigns/${campaignId}/recipients`, { params });
    return response.data;
  },

  addRecipients: async (campaignId: string, contactIds: string[]) => {
    const response = await api.post(`/campaigns/${campaignId}/recipients`, { contact_ids: contactIds });
    return response.data;
  },

  removeRecipient: async (campaignId: string, recipientId: string) => {
    const response = await api.delete(`/campaigns/${campaignId}/recipients/${recipientId}`);
    return response.data;
  },

  // Analytics
  getAnalytics: async (campaignId: string) => {
    const response = await api.get(`/campaigns/${campaignId}/analytics`);
    return response.data;
  },

  // Templates
  getTemplates: async () => {
    const response = await api.get('/campaigns/templates');
    return response.data;
  },

  createFromTemplate: async (templateId: string, data: any) => {
    const response = await api.post(`/campaigns/templates/${templateId}/create`, data);
    return response.data;
  },
};
