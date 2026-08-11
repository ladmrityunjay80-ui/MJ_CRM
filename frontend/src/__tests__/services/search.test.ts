import { describe, it, expect, vi } from 'vitest';
import { searchService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('Search Service', () => {
  it('should have globalSearch method', () => {
    expect(searchService.globalSearch).toBeDefined();
    expect(typeof searchService.globalSearch).toBe('function');
  });

  it('should have searchLeads method', () => {
    expect(searchService.searchLeads).toBeDefined();
    expect(typeof searchService.searchLeads).toBe('function');
  });

  it('should have searchContacts method', () => {
    expect(searchService.searchContacts).toBeDefined();
    expect(typeof searchService.searchContacts).toBe('function');
  });

  it('should have searchCompanies method', () => {
    expect(searchService.searchCompanies).toBeDefined();
    expect(typeof searchService.searchCompanies).toBe('function');
  });

  it('should have searchDeals method', () => {
    expect(searchService.searchDeals).toBeDefined();
    expect(typeof searchService.searchDeals).toBe('function');
  });

  it('should have searchActivities method', () => {
    expect(searchService.searchActivities).toBeDefined();
    expect(typeof searchService.searchActivities).toBe('function');
  });

  it('should have advancedSearch method', () => {
    expect(searchService.advancedSearch).toBeDefined();
    expect(typeof searchService.advancedSearch).toBe('function');
  });
});
