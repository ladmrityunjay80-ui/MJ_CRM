import { describe, it, expect, vi } from 'vitest';
import { bulkService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('Bulk Service', () => {
  it('should have bulkDelete method', () => {
    expect(bulkService.bulkDelete).toBeDefined();
    expect(typeof bulkService.bulkDelete).toBe('function');
  });

  it('should have bulkUpdate method', () => {
    expect(bulkService.bulkUpdate).toBeDefined();
    expect(typeof bulkService.bulkUpdate).toBe('function');
  });

  it('should have bulkCreate method', () => {
    expect(bulkService.bulkCreate).toBeDefined();
    expect(typeof bulkService.bulkCreate).toBe('function');
  });

  it('should have bulkExport method', () => {
    expect(bulkService.bulkExport).toBeDefined();
    expect(typeof bulkService.bulkExport).toBe('function');
  });

  it('should have bulkImport method', () => {
    expect(bulkService.bulkImport).toBeDefined();
    expect(typeof bulkService.bulkImport).toBe('function');
  });

  it('should have getOperationStatus method', () => {
    expect(bulkService.getOperationStatus).toBeDefined();
    expect(typeof bulkService.getOperationStatus).toBe('function');
  });

  it('should have getOperations method', () => {
    expect(bulkService.getOperations).toBeDefined();
    expect(typeof bulkService.getOperations).toBe('function');
  });
});
