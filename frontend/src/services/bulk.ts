import api from '../lib/api';

export interface BulkOperation {
  id: string;
  operation_type: string;
  entity_type: string;
  status: string;
  total_records: number;
  processed_records: number;
  failed_records: number;
  errors?: any[];
  created_by_id?: string;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export const bulkService = {
  // Bulk operations
  bulkDelete: async (entityType: string, ids: string[]) => {
    const response = await api.post('/bulk/delete', { entity_type: entityType, ids });
    return response.data;
  },

  bulkUpdate: async (entityType: string, ids: string[], updates: any) => {
    const response = await api.post('/bulk/update', { entity_type: entityType, ids, updates });
    return response.data;
  },

  bulkCreate: async (entityType: string, data: any[]) => {
    const response = await api.post('/bulk/create', { entity_type: entityType, data });
    return response.data;
  },

  bulkExport: async (entityType: string, ids: string[], format: 'csv' | 'json' = 'csv') => {
    const response = await api.post('/bulk/export', { entity_type: entityType, ids, format }, {
      responseType: 'blob',
    });
    return response.data;
  },

  bulkImport: async (entityType: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('entity_type', entityType);
    const response = await api.post('/bulk/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  // Operation status
  getOperationStatus: async (operationId: string) => {
    const response = await api.get(`/bulk/operations/${operationId}`);
    return response.data;
  },

  getOperations: async (params?: { page?: number; page_size?: number; entity_type?: string; status?: string }) => {
    const response = await api.get('/bulk/operations', { params });
    return response.data;
  },

  cancelOperation: async (operationId: string) => {
    const response = await api.post(`/bulk/operations/${operationId}/cancel`);
    return response.data;
  },

  // Bulk actions for specific entities
  bulkAssignLeads: async (leadIds: string[], assignedToId: string) => {
    const response = await api.post('/bulk/leads/assign', { lead_ids: leadIds, assigned_to_id: assignedToId });
    return response.data;
  },

  bulkUpdateDealStage: async (dealIds: string[], stage: string) => {
    const response = await api.post('/bulk/deals/stage', { deal_ids: dealIds, stage });
    return response.data;
  },

  bulkAddTags: async (entityType: string, ids: string[], tags: string[]) => {
    const response = await api.post('/bulk/tags/add', { entity_type: entityType, ids, tags });
    return response.data;
  },

  bulkRemoveTags: async (entityType: string, ids: string[], tags: string[]) => {
    const response = await api.post('/bulk/tags/remove', { entity_type: entityType, ids, tags });
    return response.data;
  },
};
