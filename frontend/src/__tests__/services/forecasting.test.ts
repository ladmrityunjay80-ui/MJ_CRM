import { describe, it, expect, vi } from 'vitest';
import { forecastingService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('Forecasting Service', () => {
  it('should have getRevenueForecast method', () => {
    expect(forecastingService.getRevenueForecast).toBeDefined();
    expect(typeof forecastingService.getRevenueForecast).toBe('function');
  });

  it('should have getDealForecast method', () => {
    expect(forecastingService.getDealForecast).toBeDefined();
    expect(typeof forecastingService.getDealForecast).toBe('function');
  });

  it('should have getLeadForecast method', () => {
    expect(forecastingService.getLeadForecast).toBeDefined();
    expect(typeof forecastingService.getLeadForecast).toBe('function');
  });

  it('should have getTeamForecast method', () => {
    expect(forecastingService.getTeamForecast).toBeDefined();
    expect(typeof forecastingService.getTeamForecast).toBe('function');
  });

  it('should have getForecastAccuracy method', () => {
    expect(forecastingService.getForecastAccuracy).toBeDefined();
    expect(typeof forecastingService.getForecastAccuracy).toBe('function');
  });
});
