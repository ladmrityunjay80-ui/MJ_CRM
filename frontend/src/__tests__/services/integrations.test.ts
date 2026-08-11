import { describe, it, expect, vi } from 'vitest';
import { integrationsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Integrations Service', () => {
  it('should have getAll method', () => {
    expect(integrationsService.getAll).toBeDefined();
    expect(typeof integrationsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(integrationsService.getById).toBeDefined();
    expect(typeof integrationsService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(integrationsService.create).toBeDefined();
    expect(typeof integrationsService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(integrationsService.update).toBeDefined();
    expect(typeof integrationsService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(integrationsService.delete).toBeDefined();
    expect(typeof integrationsService.delete).toBe('function');
  });

  it('should have sync method', () => {
    expect(integrationsService.sync).toBeDefined();
    expect(typeof integrationsService.sync).toBe('function');
  });

  it('should have getAvailableProviders method', () => {
    expect(integrationsService.getAvailableProviders).toBeDefined();
    expect(typeof integrationsService.getAvailableProviders).toBe('function');
  });
});
