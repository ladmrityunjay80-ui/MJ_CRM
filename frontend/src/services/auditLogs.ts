import api from '../lib/api';

export interface AuditLog {
  id: string;
  action: string;
  entity_type: string;
  entity_id: string;
  changes?: any;
  old_values?: any;
  new_values?: any;
  ip_address?: string;
  user_agent?: string;
  user_id?: string;
  organization_id: string;
  created_at: string;
}

export const auditLogsService = {
  getAll: async (params?: { 
    page?: number; 
    page_size?: number; 
    entity_type?: string; 
    action?: string; 
    user_id?: string;
    start_date?: string;
    end_date?: string;
  }) => {
    const response = await api.get('/audit-logs', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/audit-logs/${id}`);
    return response.data;
  },

  getByEntity: async (entityType: string, entityId: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get(`/audit-logs/entity/${entityType}/${entityId}`, { params });
    return response.data;
  },

  getByUser: async (userId: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get(`/audit-logs/user/${userId}`, { params });
    return response.data;
  },

  exportLogs: async (params?: { start_date?: string; end_date?: string; entity_type?: string }, format: 'csv' | 'json' = 'csv') => {
    const response = await api.get('/audit-logs/export', { 
      params: { ...params, format },
      responseType: 'blob',
    });
    return response.data;
  },

  getStatistics: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get('/audit-logs/statistics', { params });
    return response.data;
  },
};
