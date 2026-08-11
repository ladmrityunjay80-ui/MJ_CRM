import { describe, it, expect, vi } from 'vitest';
import { campaignsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Campaigns Service', () => {
  it('should have getAll method', () => {
    expect(campaignsService.getAll).toBeDefined();
    expect(typeof campaignsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(campaignsService.getById).toBeDefined();
    expect(typeof campaignsService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(campaignsService.create).toBeDefined();
    expect(typeof campaignsService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(campaignsService.update).toBeDefined();
    expect(typeof campaignsService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(campaignsService.delete).toBeDefined();
    expect(typeof campaignsService.delete).toBe('function');
  });

  it('should have send method', () => {
    expect(campaignsService.send).toBeDefined();
    expect(typeof campaignsService.send).toBe('function');
  });
});
