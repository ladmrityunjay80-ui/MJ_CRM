import api from '../lib/api';

export interface LeadScoringData {
  total_leads: number;
  high_priority: number;
  medium_priority: number;
  low_priority: number;
  top_leads: Array<{
    id: string;
    name: string;
    email?: string;
    score: number;
    factors: string[];
    priority: string;
  }>;
}

export interface DealPrediction {
  total_deals: number;
  high_probability: number;
  medium_probability: number;
  low_probability: number;
  predictions: Array<{
    id: string;
    name: string;
    value: number;
    stage: string;
    win_probability: number;
    predicted_close_date?: string;
    confidence: string;
  }>;
}

export interface ActivityRecommendation {
  type: string;
  title: string;
  description: string;
  priority: string;
  count: number;
}

export interface PerformanceTrend {
  monthly_data: Record<string, any>;
  trends: {
    deal_trend: number;
    value_trend: number;
    win_rate_trend: number;
  };
  insights: string[];
}

export interface InsightsSummary {
  health_score: number;
  health_status: string;
  key_metrics: {
    total_leads: number;
    total_deals: number;
    won_deals: number;
    lead_to_deal_ratio: number;
    win_rate: number;
  };
  recommendations: string[];
}

export const insightsService = {
  getLeadScoring: async () => {
    const response = await api.get('/insights/lead-scoring');
    return response.data as LeadScoringData;
  },

  getDealPredictions: async () => {
    const response = await api.get('/insights/deal-predictions');
    return response.data as DealPrediction;
  },

  getActivityRecommendations: async () => {
    const response = await api.get('/insights/activity-recommendations');
    return response.data as { total_recommendations: number; recommendations: ActivityRecommendation[] };
  },

  getPerformanceTrends: async () => {
    const response = await api.get('/insights/performance-trends');
    return response.data as PerformanceTrend;
  },

  getSummary: async () => {
    const response = await api.get('/insights/summary');
    return response.data as InsightsSummary;
  },

  // Mobile insights
  getMobileInsights: async () => {
    const response = await api.get('/mobile/insights');
    return response.data;
  },

  // AI-powered features
  getSmartSuggestions: async (context: string) => {
    const response = await api.get('/insights/suggestions', { params: { context } });
    return response.data;
  },

  getAnomalyDetection: async (entityType: string, params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get(`/insights/anomalies/${entityType}`, { params });
    return response.data;
  },

  getPredictiveAnalytics: async (metric: string, params?: { period?: string; forecast_days?: number }) => {
    const response = await api.get(`/insights/predict/${metric}`, { params });
    return response.data;
  },
};
