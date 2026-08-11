import api from '../lib/api';

export interface ForecastData {
  period: string;
  forecasted_revenue: number;
  actual_revenue?: number;
  confidence: number;
  factors: any[];
}

export const forecastingService = {
  getRevenueForecast: async (params?: { 
    period: 'monthly' | 'quarterly' | 'yearly';
    months_ahead?: number;
    include_historical?: boolean;
  }) => {
    const response = await api.get('/forecasting/revenue', { params });
    return response.data;
  },

  getDealForecast: async (params?: { 
    stage?: string;
    probability_threshold?: number;
    months_ahead?: number;
  }) => {
    const response = await api.get('/forecasting/deals', { params });
    return response.data;
  },

  getLeadForecast: async (params?: { 
    source?: string;
    months_ahead?: number;
  }) => {
    const response = await api.get('/forecasting/leads', { params });
    return response.data;
  },

  getTeamForecast: async (params?: { 
    user_id?: string;
    period?: string;
    months_ahead?: number;
  }) => {
    const response = await api.get('/forecasting/team', { params });
    return response.data;
  },

  getForecastAccuracy: async (params?: { 
    start_date?: string;
    end_date?: string;
  }) => {
    const response = await api.get('/forecasting/accuracy', { params });
    return response.data;
  },

  getForecastFactors: async (forecastType: string) => {
    const response = await api.get(`/forecasting/factors/${forecastType}`);
    return response.data;
  },

  adjustForecast: async (forecastId: string, adjustments: any) => {
    const response = await api.post(`/forecasting/${forecastId}/adjust`, adjustments);
    return response.data;
  },
};
