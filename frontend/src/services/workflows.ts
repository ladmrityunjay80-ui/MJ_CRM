import api from '../lib/api';

export interface Workflow {
  id: string;
  name: string;
  description?: string;
  trigger_type: string;
  trigger_config: any;
  is_active: boolean;
  organization_id: string;
  created_by_id?: string;
  created_at: string;
  updated_at: string;
}

export interface WorkflowAction {
  id: string;
  workflow_id: string;
  action_type: string;
  action_config: any;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface WorkflowExecution {
  id: string;
  workflow_id: string;
  status: string;
  input_data: any;
  output_data: any;
  error_message?: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export const workflowsService = {
  getAll: async (params?: { page?: number; page_size?: number; is_active?: boolean }) => {
    const response = await api.get('/workflows', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/workflows/${id}`);
    return response.data;
  },

  create: async (data: Partial<Workflow>) => {
    const response = await api.post('/workflows', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Workflow>) => {
    const response = await api.put(`/workflows/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/workflows/${id}`);
    return response.data;
  },

  execute: async (id: string, inputData?: any) => {
    const response = await api.post(`/workflows/${id}/execute`, { input_data: inputData });
    return response.data;
  },

  getExecutions: async (workflowId: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get(`/workflows/${workflowId}/executions`, { params });
    return response.data;
  },

  toggleActive: async (id: string, isActive: boolean) => {
    const response = await api.patch(`/workflows/${id}/toggle`, { is_active: isActive });
    return response.data;
  },
};
