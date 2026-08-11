import { describe, it, expect, vi } from 'vitest';
import { insightsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('Insights Service', () => {
  it('should have getLeadScoring method', () => {
    expect(insightsService.getLeadScoring).toBeDefined();
    expect(typeof insightsService.getLeadScoring).toBe('function');
  });

  it('should have getDealPredictions method', () => {
    expect(insightsService.getDealPredictions).toBeDefined();
    expect(typeof insightsService.getDealPredictions).toBe('function');
  });

  it('should have getActivityRecommendations method', () => {
    expect(insightsService.getActivityRecommendations).toBeDefined();
    expect(typeof insightsService.getActivityRecommendations).toBe('function');
  });

  it('should have getPerformanceTrends method', () => {
    expect(insightsService.getPerformanceTrends).toBeDefined();
    expect(typeof insightsService.getPerformanceTrends).toBe('function');
  });

  it('should have getSummary method', () => {
    expect(insightsService.getSummary).toBeDefined();
    expect(typeof insightsService.getSummary).toBe('function');
  });
});
