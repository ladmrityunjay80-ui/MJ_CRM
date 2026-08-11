import { describe, it, expect, vi } from 'vitest';
import { dealsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Deals Service', () => {
  it('should have getAll method', () => {
    expect(dealsService.getAll).toBeDefined();
    expect(typeof dealsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(dealsService.getById).toBeDefined();
    expect(typeof dealsService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(dealsService.create).toBeDefined();
    expect(typeof dealsService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(dealsService.update).toBeDefined();
    expect(typeof dealsService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(dealsService.delete).toBeDefined();
    expect(typeof dealsService.delete).toBe('function');
  });
});
