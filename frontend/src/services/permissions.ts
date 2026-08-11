import api from '../lib/api';

export interface Permission {
  id: string;
  name: string;
  description?: string;
  resource: string;
  action: string;
  conditions?: any;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export interface RolePermission {
  id: string;
  role: string;
  permission_id: string;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export const permissionsService = {
  getAll: async (params?: { page?: number; page_size?: number; resource?: string }) => {
    const response = await api.get('/permissions', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/permissions/${id}`);
    return response.data;
  },

  create: async (data: Partial<Permission>) => {
    const response = await api.post('/permissions', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Permission>) => {
    const response = await api.put(`/permissions/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await api.delete(`/permissions/${id}`);
    return response.data;
  },

  // Role Permissions
  getRolePermissions: async (role: string) => {
    const response = await api.get(`/permissions/roles/${role}`);
    return response.data;
  },

  assignPermissionToRole: async (role: string, permissionId: string) => {
    const response = await api.post(`/permissions/roles/${role}/permissions`, { permission_id: permissionId });
    return response.data;
  },

  removePermissionFromRole: async (role: string, permissionId: string) => {
    const response = await api.delete(`/permissions/roles/${role}/permissions/${permissionId}`);
    return response.data;
  },

  checkPermission: async (resource: string, action: string) => {
    const response = await api.get('/permissions/check', { params: { resource, action } });
    return response.data;
  },

  getUserPermissions: async () => {
    const response = await api.get('/permissions/user');
    return response.data;
  },
};
