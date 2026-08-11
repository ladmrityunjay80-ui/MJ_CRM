import { describe, it, expect, vi } from 'vitest';
import { emailsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Emails Service', () => {
  it('should have getAll method', () => {
    expect(emailsService.getAll).toBeDefined();
    expect(typeof emailsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(emailsService.getById).toBeDefined();
    expect(typeof emailsService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(emailsService.create).toBeDefined();
    expect(typeof emailsService.create).toBe('function');
  });

  it('should have send method', () => {
    expect(emailsService.send).toBeDefined();
    expect(typeof emailsService.send).toBe('function');
  });

  it('should have schedule method', () => {
    expect(emailsService.schedule).toBeDefined();
    expect(typeof emailsService.schedule).toBe('function');
  });

  it('should have getTemplates method', () => {
    expect(emailsService.getTemplates).toBeDefined();
    expect(typeof emailsService.getTemplates).toBe('function');
  });

  it('should have createTemplate method', () => {
    expect(emailsService.createTemplate).toBeDefined();
    expect(typeof emailsService.createTemplate).toBe('function');
  });
});
