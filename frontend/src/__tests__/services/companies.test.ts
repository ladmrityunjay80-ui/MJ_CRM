import { describe, it, expect, vi } from 'vitest';
import { companiesService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Companies Service', () => {
  it('should have getAll method', () => {
    expect(companiesService.getAll).toBeDefined();
    expect(typeof companiesService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(companiesService.getById).toBeDefined();
    expect(typeof companiesService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(companiesService.create).toBeDefined();
    expect(typeof companiesService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(companiesService.update).toBeDefined();
    expect(typeof companiesService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(companiesService.delete).toBeDefined();
    expect(typeof companiesService.delete).toBe('function');
  });
});
