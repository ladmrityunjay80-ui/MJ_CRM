export interface User {
  id: string;
  email: string;
  full_name: string;
  phone?: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  avatar_url?: string;
  organization_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Lead {
  id: string;
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  company?: string;
  job_title?: string;
  status: string;
  source: string;
  estimated_value?: number;
  probability?: number;
  notes?: string;
  tags?: string[];
  organization_id: string;
  assigned_to_id?: string;
  contact_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Contact {
  id: string;
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  mobile?: string;
  job_title?: string;
  department?: string;
  linkedin?: string;
  twitter?: string;
  notes?: string;
  tags?: string[];
  avatar_url?: string;
  organization_id: string;
  company_id?: string;
  created_by_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Company {
  id: string;
  name: string;
  website?: string;
  industry?: string;
  size?: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  postal_code?: string;
  phone?: string;
  email?: string;
  notes?: string;
  tags?: string[];
  logo_url?: string;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export interface Deal {
  id: string;
  name: string;
  description?: string;
  value: number;
  currency: string;
  probability?: number;
  expected_close_date?: string;
  actual_close_date?: string;
  stage: string;
  lost_reason?: string;
  notes?: string;
  tags?: string[];
  organization_id: string;
  company_id?: string;
  assigned_to_id?: string;
  contact_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Activity {
  id: string;
  type: string;
  status: string;
  subject: string;
  description?: string;
  location?: string;
  scheduled_at?: string;
  duration_minutes?: number;
  completed_at?: string;
  reminder_minutes_before?: number;
  reminder_sent: boolean;
  notes?: string;
  organization_id: string;
  created_by_id?: string;
  lead_id?: string;
  contact_id?: string;
  deal_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: string;
  name: string;
  description?: string;
  sku?: string;
  type: string;
  price: number;
  currency: string;
  quantity_in_stock?: number;
  low_stock_threshold?: number;
  notes?: string;
  tags?: string[];
  is_active: boolean;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
}
