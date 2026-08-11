import api from '../lib/api';

export interface ReportData {
  [key: string]: any;
}

export const reportsService = {
  // Sales Performance
  getSalesPerformance: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get('/reports/sales-performance', { params });
    return response.data;
  },

  // Lead Conversion
  getLeadConversion: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get('/reports/lead-conversion', { params });
    return response.data;
  },

  // Activity Summary
  getActivitySummary: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get('/reports/activity-summary', { params });
    return response.data;
  },

  // Revenue Trend
  getRevenueTrend: async (params?: { start_date?: string; end_date?: string; period?: string }) => {
    const response = await api.get('/reports/revenue-trend', { params });
    return response.data;
  },

  // Team Performance
  getTeamPerformance: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get('/reports/team-performance', { params });
    return response.data;
  },

  // Custom Reports
  createCustomReport: async (data: { name: string; description?: string; query: any; filters?: any }) => {
    const response = await api.post('/reports/custom', data);
    return response.data;
  },

  getCustomReports: async (params?: { page?: number; page_size?: number }) => {
    const response = await api.get('/reports/custom', { params });
    return response.data;
  },

  getCustomReportById: async (id: string, params?: any) => {
    const response = await api.get(`/reports/custom/${id}`, { params });
    return response.data;
  },

  updateCustomReport: async (id: string, data: any) => {
    const response = await api.put(`/reports/custom/${id}`, data);
    return response.data;
  },

  deleteCustomReport: async (id: string) => {
    const response = await api.delete(`/reports/custom/${id}`);
    return response.data;
  },

  runCustomReport: async (id: string, parameters?: any) => {
    const response = await api.post(`/reports/custom/${id}/run`, parameters);
    return response.data;
  },

  // Export Reports
  exportReport: async (reportType: string, params?: any, format: 'csv' | 'pdf' | 'excel' = 'csv') => {
    const response = await api.get(`/reports/${reportType}/export`, {
      params: { ...params, format },
      responseType: 'blob',
    });
    return response.data;
  },

  // Schedule Reports
  scheduleReport: async (reportId: string, schedule: { frequency: string; day?: string; time?: string; recipients?: string[] }) => {
    const response = await api.post(`/reports/${reportId}/schedule`, schedule);
    return response.data;
  },

  getScheduledReports: async () => {
    const response = await api.get('/reports/scheduled');
    return response.data;
  },
};
