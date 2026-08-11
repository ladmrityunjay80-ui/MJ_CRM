import { describe, it, expect, vi } from 'vitest';
import { workflowsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
    patch: vi.fn(),
  },
}));

describe('Workflows Service', () => {
  it('should have getAll method', () => {
    expect(workflowsService.getAll).toBeDefined();
    expect(typeof workflowsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(workflowsService.getById).toBeDefined();
    expect(typeof workflowsService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(workflowsService.create).toBeDefined();
    expect(typeof workflowsService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(workflowsService.update).toBeDefined();
    expect(typeof workflowsService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(workflowsService.delete).toBeDefined();
    expect(typeof workflowsService.delete).toBe('function');
  });

  it('should have execute method', () => {
    expect(workflowsService.execute).toBeDefined();
    expect(typeof workflowsService.execute).toBe('function');
  });

  it('should have toggleActive method', () => {
    expect(workflowsService.toggleActive).toBeDefined();
    expect(typeof workflowsService.toggleActive).toBe('function');
  });
});
