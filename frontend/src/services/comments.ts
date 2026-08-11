import api from '../lib/api';

export interface Comment {
  id: string;
  content: string;
  entity_type: string;
  entity_id: string;
  parent_id?: string;
  created_by_id?: string;
  created_by?: {
    id: string;
    full_name: string;
    email: string;
    avatar_url?: string;
  };
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export const commentsService = {
  getByEntity: async (entityType: string, entityId: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get(`/comments/${entityType}/${entityId}`, { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/comments/${id}`);
    return response.data;
  },

  create: async (data: { content: string; entity_type: string; entity_id: string; parent_id?: string }) => {
    const response = await api.post('/comments', data);
    return response.data;
  },

  update: async (id: string, data: { content: string }) => {
    const response = await api.put(`/comments/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/comments/${id}`);
    return response.data;
  },

  getReplies: async (commentId: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get(`/comments/${commentId}/replies`, { params });
    return response.data;
  },
};
