import { describe, it, expect, vi } from 'vitest';
import { leadsService } from '../../services';

// Mock the API module
vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Leads Service', () => {
  it('should have getAll method', () => {
    expect(leadsService.getAll).toBeDefined();
    expect(typeof leadsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(leadsService.getById).toBeDefined();
    expect(typeof leadsService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(leadsService.create).toBeDefined();
    expect(typeof leadsService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(leadsService.update).toBeDefined();
    expect(typeof leadsService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(leadsService.delete).toBeDefined();
    expect(typeof leadsService.delete).toBe('function');
  });
});
