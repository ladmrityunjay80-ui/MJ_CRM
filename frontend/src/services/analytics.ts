import api from '../lib/api';

export interface Report {
  id: string;
  name: string;
  description?: string;
  report_type: string;
  config: any;
  schedule?: string;
  last_run_at?: string;
  organization_id: string;
  created_by_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Dashboard {
  id: string;
  name: string;
  description?: string;
  layout: any;
  organization_id: string;
  created_by_id?: string;
  created_at: string;
  updated_at: string;
}

export const analyticsService = {
  // Reports
  getAllReports: async (params?: { page?: number; page_size?: number; report_type?: string }) => {
    const response = await api.get('/analytics/reports', { params });
    return response.data;
  },

  getReportById: async (id: string) => {
    const response = await api.get(`/analytics/reports/${id}`);
    return response.data;
  },

  createReport: async (data: Partial<Report>) => {
    const response = await api.post('/analytics/reports', data);
    return response.data;
  },

  updateReport: async (id: string, data: Partial<Report>) => {
    const response = await api.put(`/analytics/reports/${id}`, data);
    return response.data;
  },

  deleteReport: async (id: string) => {
    const response = await api.delete(`/analytics/reports/${id}`);
    return response.data;
  },

  runReport: async (id: string, params?: any) => {
    const response = await api.post(`/analytics/reports/${id}/run`, params);
    return response.data;
  },

  // Dashboards
  getAllDashboards: async (params?: { page?: number; page_size?: number }) => {
    const response = await api.get('/analytics/dashboards', { params });
    return response.data;
  },

  getDashboardById: async (id: string) => {
    const response = await api.get(`/analytics/dashboards/${id}`);
    return response.data;
  },

  createDashboard: async (data: Partial<Dashboard>) => {
    const response = await api.post('/analytics/dashboards', data);
    return response.data;
  },

  updateDashboard: async (id: string, data: Partial<Dashboard>) => {
    const response = await api.put(`/analytics/dashboards/${id}`, data);
    return response.data;
  },

  deleteDashboard: async (id: string) => {
    const response = await api.delete(`/analytics/dashboards/${id}`);
    return response.data;
  },

  // Analytics Data
  getSalesAnalytics: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get('/analytics/sales', { params });
    return response.data;
  },

  getLeadAnalytics: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get('/analytics/leads', { params });
    return response.data;
  },

  getActivityAnalytics: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get('/analytics/activities', { params });
    return response.data;
  },
};
