import { describe, it, expect, vi } from 'vitest';
import { reportsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Reports Service', () => {
  it('should have getSalesPerformance method', () => {
    expect(reportsService.getSalesPerformance).toBeDefined();
    expect(typeof reportsService.getSalesPerformance).toBe('function');
  });

  it('should have getLeadConversion method', () => {
    expect(reportsService.getLeadConversion).toBeDefined();
    expect(typeof reportsService.getLeadConversion).toBe('function');
  });

  it('should have getActivitySummary method', () => {
    expect(reportsService.getActivitySummary).toBeDefined();
    expect(typeof reportsService.getActivitySummary).toBe('function');
  });

  it('should have getRevenueTrend method', () => {
    expect(reportsService.getRevenueTrend).toBeDefined();
    expect(typeof reportsService.getRevenueTrend).toBe('function');
  });

  it('should have getTeamPerformance method', () => {
    expect(reportsService.getTeamPerformance).toBeDefined();
    expect(typeof reportsService.getTeamPerformance).toBe('function');
  });

  it('should have createCustomReport method', () => {
    expect(reportsService.createCustomReport).toBeDefined();
    expect(typeof reportsService.createCustomReport).toBe('function');
  });
});
