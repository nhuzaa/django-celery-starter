export interface Device {
  id: number;
  name: string;
  device_type: 'IMPLANT' | 'DIAGNOSTIC' | 'MONITORING' | 'THERAPEUTIC';
  model_number: string;
  manufacturer: string;
  description: string;
  assigned_to?: number;
  assigned_to_name?: string;
  created_at: string;
  updated_at: string;
}

export interface TestProtocol {
  id: number;
  name: string;
  version: string;
  description: string;
  status: 'DRAFT' | 'REVIEW' | 'APPROVED' | 'ARCHIVED';
  created_by: number;
  created_by_name: string;
  devices: number[];
  created_at: string;
  updated_at: string;
}

export interface TestResult {
  id: number;
  device: number;
  device_name: string;
  protocol: number;
  protocol_name: string;
  performed_by: number;
  performed_by_name: string;
  status: 'PASS' | 'FAIL' | 'IN_PROGRESS' | 'INVALID';
  start_time: string;
  end_time?: string;
  notes?: string;
  data?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  is_staff: boolean;
  is_active: boolean;
  date_joined: string;
} 