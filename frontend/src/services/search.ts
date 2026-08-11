import api from '../lib/api';

export interface SearchResult {
  type: string;
  id: string;
  title: string;
  description?: string;
  score: number;
  data: any;
}

export const searchService = {
  globalSearch: async (query: string, params?: { entity_types?: string[]; page?: number; page_size?: number }) => {
    const response = await api.get('/search', { params: { q: query, ...params } });
    return response.data;
  },

  searchLeads: async (query: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get('/search/leads', { params: { q: query, ...params } });
    return response.data;
  },

  searchContacts: async (query: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get('/search/contacts', { params: { q: query, ...params } });
    return response.data;
  },

  searchCompanies: async (query: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get('/search/companies', { params: { q: query, ...params } });
    return response.data;
  },

  searchDeals: async (query: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get('/search/deals', { params: { q: query, ...params } });
    return response.data;
  },

  searchActivities: async (query: string, params?: { page?: number; page_size?: number }) => {
    const response = await api.get('/search/activities', { params: { q: query, ...params } });
    return response.data;
  },

  advancedSearch: async (filters: any, params?: { page?: number; page_size?: number }) => {
    const response = await api.post('/search/advanced', filters, { params });
    return response.data;
  },

  getRecentSearches: async () => {
    const response = await api.get('/search/recent');
    return response.data;
  },

  saveSearch: async (name: string, query: string, filters?: any) => {
    const response = await api.post('/search/save', { name, query, filters });
    return response.data;
  },

  getSavedSearches: async () => {
    const response = await api.get('/search/saved');
    return response.data;
  },
};
