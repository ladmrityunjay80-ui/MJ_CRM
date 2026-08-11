import { describe, it, expect, vi } from 'vitest';
import { contactsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Contacts Service', () => {
  it('should have getAll method', () => {
    expect(contactsService.getAll).toBeDefined();
    expect(typeof contactsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(contactsService.getById).toBeDefined();
    expect(typeof contactsService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(contactsService.create).toBeDefined();
    expect(typeof contactsService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(contactsService.update).toBeDefined();
    expect(typeof contactsService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(contactsService.delete).toBeDefined();
    expect(typeof contactsService.delete).toBe('function');
  });
});
