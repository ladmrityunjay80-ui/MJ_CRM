import { describe, it, expect, vi } from 'vitest';
import { auditLogsService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
  },
}));

describe('Audit Logs Service', () => {
  it('should have getAll method', () => {
    expect(auditLogsService.getAll).toBeDefined();
    expect(typeof auditLogsService.getAll).toBe('function');
  });

  it('should have getById method', () => {
    expect(auditLogsService.getById).toBeDefined();
    expect(typeof auditLogsService.getById).toBe('function');
  });

  it('should have getByEntity method', () => {
    expect(auditLogsService.getByEntity).toBeDefined();
    expect(typeof auditLogsService.getByEntity).toBe('function');
  });

  it('should have getByUser method', () => {
    expect(auditLogsService.getByUser).toBeDefined();
    expect(typeof auditLogsService.getByUser).toBe('function');
  });

  it('should have exportLogs method', () => {
    expect(auditLogsService.exportLogs).toBeDefined();
    expect(typeof auditLogsService.exportLogs).toBe('function');
  });

  it('should have getStatistics method', () => {
    expect(auditLogsService.getStatistics).toBeDefined();
    expect(typeof auditLogsService.getStatistics).toBe('function');
  });
});
