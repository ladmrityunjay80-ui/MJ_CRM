import api from '../lib/api';

export interface Document {
  id: string;
  name: string;
  description?: string;
  document_type: string;
  file_url: string;
  file_size: number;
  file_type: string;
  entity_type?: string;
  entity_id?: string;
  uploaded_by_id?: string;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export const documentsService = {
  getAll: async (params?: { page?: number; page_size?: number; document_type?: string; entity_type?: string }) => {
    const response = await api.get('/documents', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/documents/${id}`);
    return response.data;
  },

  upload: async (file: File, metadata?: { description?: string; document_type?: string; entity_type?: string; entity_id?: string }) => {
    const formData = new FormData();
    formData.append('file', file);
    if (metadata) {
      Object.entries(metadata).forEach(([key, value]) => {
        if (value) formData.append(key, value);
      });
    }
    const response = await api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  update: async (id: string, data: Partial<Document>) => {
    const response = await api.put(`/documents/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/documents/${id}`);
    return response.data;
  },

  download: async (id: string) => {
    const response = await api.get(`/documents/${id}/download`, { responseType: 'blob' });
    return response.data;
  },

  getByEntity: async (entityType: string, entityId: string) => {
    const response = await api.get(`/documents/entity/${entityType}/${entityId}`);
    return response.data;
  },
};
