import api from '../lib/api';

export const importExportService = {
  // Export functions
  exportLeads: async (format: 'csv' | 'json' = 'csv') => {
    const response = await api.get('/import-export/export/leads', {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },

  exportContacts: async (format: 'csv' | 'json' = 'csv') => {
    const response = await api.get('/import-export/export/contacts', {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },

  exportCompanies: async (format: 'csv' | 'json' = 'csv') => {
    const response = await api.get('/import-export/export/companies', {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },

  exportDeals: async (format: 'csv' | 'json' = 'csv') => {
    const response = await api.get('/import-export/export/deals', {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },

  exportActivities: async (format: 'csv' | 'json' = 'csv') => {
    const response = await api.get('/import-export/export/activities', {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },

  exportProducts: async (format: 'csv' | 'json' = 'csv') => {
    const response = await api.get('/import-export/export/products', {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },

  // Import functions
  importLeads: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/import-export/import/leads', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  importContacts: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/import-export/import/contacts', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  importCompanies: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/import-export/import/companies', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  importDeals: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/import-export/import/deals', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  importActivities: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/import-export/import/activities', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  importProducts: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/import-export/import/products', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  // Import status
  getImportStatus: async (importId: string) => {
    const response = await api.get(`/import-export/import/status/${importId}`);
    return response.data;
  },
};
