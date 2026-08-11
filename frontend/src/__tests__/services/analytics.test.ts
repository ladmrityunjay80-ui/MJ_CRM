import { describe, it, expect, vi } from 'vitest';
import { analyticsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Analytics Service', () => {
  it('should have getAllReports method', () => {
    expect(analyticsService.getAllReports).toBeDefined();
    expect(typeof analyticsService.getAllReports).toBe('function');
  });

  it('should have getReportById method', () => {
    expect(analyticsService.getReportById).toBeDefined();
    expect(typeof analyticsService.getReportById).toBe('function');
  });

  it('should have createReport method', () => {
    expect(analyticsService.createReport).toBeDefined();
    expect(typeof analyticsService.createReport).toBe('function');
  });

  it('should have updateReport method', () => {
    expect(analyticsService.updateReport).toBeDefined();
    expect(typeof analyticsService.updateReport).toBe('function');
  });

  it('should have deleteReport method', () => {
    expect(analyticsService.deleteReport).toBeDefined();
    expect(typeof analyticsService.deleteReport).toBe('function');
  });

  it('should have getSalesAnalytics method', () => {
    expect(analyticsService.getSalesAnalytics).toBeDefined();
    expect(typeof analyticsService.getSalesAnalytics).toBe('function');
  });

  it('should have getLeadAnalytics method', () => {
    expect(analyticsService.getLeadAnalytics).toBeDefined();
    expect(typeof analyticsService.getLeadAnalytics).toBe('function');
  });
});
