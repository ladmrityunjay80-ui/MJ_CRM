import api from '../lib/api';

export interface Email {
  id: string;
  subject: string;
  body: string;
  from_email: string;
  to_email: string;
  cc_email?: string;
  bcc_email?: string;
  status: string;
  sent_at?: string;
  scheduled_at?: string;
  organization_id: string;
  created_by_id?: string;
  created_at: string;
  updated_at: string;
}

export interface EmailTemplate {
  id: string;
  name: string;
  subject: string;
  body: string;
  variables?: string[];
  is_active: boolean;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export const emailsService = {
  getAll: async (params?: { page?: number; page_size?: number; status?: string }) => {
    const response = await api.get('/emails', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/emails/${id}`);
    return response.data;
  },

  create: async (data: Partial<Email>) => {
    const response = await api.post('/emails', data);
    return response.data;
  },

  send: async (data: { subject: string; body: string; to_email: string; cc_email?: string; bcc_email?: string }) => {
    const response = await api.post('/emails/send', data);
    return response.data;
  },

  schedule: async (data: { subject: string; body: string; to_email: string; scheduled_at: string }) => {
    const response = await api.post('/emails/schedule', data);
    return response.data;
  },

  // Email Templates
  getTemplates: async (params?: { page?: number; page_size?: number }) => {
    const response = await api.get('/emails/templates', { params });
    return response.data;
  },

  getTemplateById: async (id: string) => {
    const response = await api.get(`/emails/templates/${id}`);
    return response.data;
  },

  createTemplate: async (data: Partial<EmailTemplate>) => {
    const response = await api.post('/emails/templates', data);
    return response.data;
  },

  updateTemplate: async (id: string, data: Partial<EmailTemplate>) => {
    const response = await api.put(`/emails/templates/${id}`, data);
    return response.data;
  },

  deleteTemplate: async (id: string) => {
    const response = await api.delete(`/emails/templates/${id}`);
    return response.data;
  },

  useTemplate: async (templateId: string, variables: Record<string, string>) => {
    const response = await api.post(`/emails/templates/${templateId}/use`, { variables });
    return response.data;
  },
};
