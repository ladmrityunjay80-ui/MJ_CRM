import { describe, it, expect, vi } from 'vitest';
import { activitiesService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Activities Service', () => {
  it('should have getAll method', () => {
    expect(activitiesService.getAll).toBeDefined();
    expect(typeof activitiesService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(activitiesService.getById).toBeDefined();
    expect(typeof activitiesService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(activitiesService.create).toBeDefined();
    expect(typeof activitiesService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(activitiesService.update).toBeDefined();
    expect(typeof activitiesService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(activitiesService.delete).toBeDefined();
    expect(typeof activitiesService.delete).toBe('function');
  });
});
