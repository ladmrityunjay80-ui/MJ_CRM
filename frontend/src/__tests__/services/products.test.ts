import { describe, it, expect, vi } from 'vitest';
import { productsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Products Service', () => {
  it('should have getAll method', () => {
    expect(productsService.getAll).toBeDefined();
    expect(typeof productsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(productsService.getById).toBeDefined();
    expect(typeof productsService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(productsService.create).toBeDefined();
    expect(typeof productsService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(productsService.update).toBeDefined();
    expect(typeof productsService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(productsService.delete).toBeDefined();
    expect(typeof productsService.delete).toBe('function');
  });
});
