import { describe, it, expect, vi } from 'vitest';
import { commentsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Comments Service', () => {
  it('should have getByEntity method', () => {
    expect(commentsService.getByEntity).toBeDefined();
    expect(typeof commentsService.getByEntity).toBe('function');
  });

  it('should have getById method', () => {
    expect(commentsService.getById).toBeDefined();
    expect(typeof commentsService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(commentsService.create).toBeDefined();
    expect(typeof commentsService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(commentsService.update).toBeDefined();
    expect(typeof commentsService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(commentsService.delete).toBeDefined();
    expect(typeof commentsService.delete).toBe('function');
  });

  it('should have getReplies method', () => {
    expect(commentsService.getReplies).toBeDefined();
    expect(typeof commentsService.getReplies).toBe('function');
  });
});
