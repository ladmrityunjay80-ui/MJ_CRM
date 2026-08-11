import { describe, it, expect, vi } from 'vitest';
import { permissionsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('Permissions Service', () => {
  it('should have getAll method', () => {
    expect(permissionsService.getAll).toBeDefined();
    expect(typeof permissionsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(permissionsService.getById).toBeDefined();
    expect(typeof permissionsService.getById).toBe('function');
  });

  it('should have create method', () => {
    expect(permissionsService.create).toBeDefined();
    expect(typeof permissionsService.create).toBe('function');
  });

  it('should have update method', () => {
    expect(permissionsService.update).toBeDefined();
    expect(typeof permissionsService.update).toBe('function');
  });

  it('should have delete method', () => {
    expect(permissionsService.delete).toBeDefined();
    expect(typeof permissionsService.delete).toBe('function');
  });

  it('should have getRolePermissions method', () => {
    expect(permissionsService.getRolePermissions).toBeDefined();
    expect(typeof permissionsService.getRolePermissions).toBe('function');
  });

  it('should have checkPermission method', () => {
    expect(permissionsService.checkPermission).toBeDefined();
    expect(typeof permissionsService.checkPermission).toBe('function');
  });

  it('should have getUserPermissions method', () => {
    expect(permissionsService.getUserPermissions).toBeDefined();
    expect(typeof permissionsService.getUserPermissions).toBe('function');
  });
});
