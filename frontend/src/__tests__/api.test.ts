import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import api from '../lib/api';

describe('API Client', () => {
  beforeEach(() => {
    // Reset any necessary state before each test
  });

  afterEach(() => {
    // Clean up after each test
  });

  it('should have correct base URL configuration', () => {
    expect(api.defaults.baseURL).toBeDefined();
  });

  it('should have default headers configured', () => {
    expect(api.defaults.headers.common['Content-Type']).toBe('application/json');
  });

  it('should have timeout configured', () => {
    expect(api.defaults.timeout).toBeDefined();
  });
});
