import { describe, it, expect, vi } from 'vitest';
import { documentsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Documents Service', () => {
  it('should have getAll method', () => {
    expect(documentsService.getAll).toBeDefined();
    expect(typeof documentsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(documentsService.getById).toBeDefined();
    expect(typeof documentsService.getById).toBe('function');
  });

  it('should have upload method', () => {
    expect(documentsService.upload).toBeDefined();
    expect(typeof documentsService.upload).toBe('function');
  });

  it('should have update method', () => {
    expect(documentsService.update).toBeDefined();
    expect(typeof documentsService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(documentsService.delete).toBeDefined();
    expect(typeof documentsService.delete).toBe('function');
  });

  it('should have download method', () => {
    expect(documentsService.download).toBeDefined();
    expect(typeof documentsService.download).toBe('function');
  });
});
