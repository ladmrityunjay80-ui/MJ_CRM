import { describe, it, expect, vi } from 'vitest';
import { webhooksService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Webhooks Service', () => {
  it('should have getAll method', () => {
    expect(webhooksService.getAll).toBeDefined();
    expect(typeof webhooksService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(webhooksService.getById).toBeDefined();
    expect(typeof webhooksService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(webhooksService.create).toBeDefined();
    expect(typeof webhooksService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(webhooksService.update).toBeDefined();
    expect(typeof webhooksService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(webhooksService.delete).toBeDefined();
    expect(typeof webhooksService.delete).toBe('function');
  });

  it('should have test method', () => {
    expect(webhooksService.test).toBeDefined();
    expect(typeof webhooksService.test).toBe('function');
  });

  it('should have getLogs method', () => {
    expect(webhooksService.getLogs).toBeDefined();
    expect(typeof webhooksService.getLogs).toBe('function');
  });
});
