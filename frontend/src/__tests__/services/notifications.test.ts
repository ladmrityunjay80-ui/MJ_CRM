import { describe, it, expect, vi } from 'vitest';
import { notificationsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
    patch: vi.fn(),
  },
}));

describe('Notifications Service', () => {
  it('should have getAll method', () => {
    expect(notificationsService.getAll).toBeDefined();
    expect(typeof notificationsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(notificationsService.getById).toBeDefined();
    expect(typeof notificationsService.getById).toBe('function');
  });

  it('should have markAsRead method', () => {
    expect(notificationsService.markAsRead).toBeDefined();
    expect(typeof notificationsService.markAsRead).toBe('function');
  });

  it('should have markAllAsRead method', () => {
    expect(notificationsService.markAllAsRead).toBeDefined();
    expect(typeof notificationsService.markAllAsRead).toBe('function');
  });

  it('should have delete method', () => {
    expect(notificationsService.delete).toBeDefined();
    expect(typeof notificationsService.delete).toBe('function');
  });

  it('should have getUnreadCount method', () => {
    expect(notificationsService.getUnreadCount).toBeDefined();
    expect(typeof notificationsService.getUnreadCount).toBe('function');
  });
});
