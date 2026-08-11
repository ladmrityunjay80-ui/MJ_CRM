import { describe, it, expect, vi } from 'vitest';
import { importExportService } from '../../services';

vi.mock('../../lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('Import/Export Service', () => {
  it('should have exportLeads method', () => {
    expect(importExportService.exportLeads).toBeDefined();
    expect(typeof importExportService.exportLeads).toBe('function');
  });

  it('should have exportContacts method', () => {
    expect(importExportService.exportContacts).toBeDefined();
    expect(typeof importExportService.exportContacts).toBe('function');
  });

  it('should have exportCompanies method', () => {
    expect(importExportService.exportCompanies).toBeDefined();
    expect(typeof importExportService.exportCompanies).toBe('function');
  });

  it('should have exportDeals method', () => {
    expect(importExportService.exportDeals).toBeDefined();
    expect(typeof importExportService.exportDeals).toBe('function');
  });

  it('should have exportActivities method', () => {
    expect(importExportService.exportActivities).toBeDefined();
    expect(typeof importExportService.exportActivities).toBe('function');
  });

  it('should have exportProducts method', () => {
    expect(importExportService.exportProducts).toBeDefined();
    expect(typeof importExportService.exportProducts).toBe('function');
  });

  it('should have importLeads method', () => {
    expect(importExportService.importLeads).toBeDefined();
    expect(typeof importExportService.importLeads).toBe('function');
  });

  it('should have importContacts method', () => {
    expect(importExportService.importContacts).toBeDefined();
    expect(typeof importExportService.importContacts).toBe('function');
  });
});
