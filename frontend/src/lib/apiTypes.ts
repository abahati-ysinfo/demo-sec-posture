/**
 * Type definitions for API responses
 * Provides type safety for commonly used API endpoints
 */

export interface User {
  id: string;
  email: string;
  full_name: string;
  company_name: string;
  is_active: boolean;
  is_admin: boolean;
  is_protected: boolean;
  created_at: string;
  updated_at: string;
}

export interface Assessment {
  id: string;
  user_id: string;
  status: 'in_progress' | 'completed';
  progress_percentage: number;
  attempt_number: number;
  started_at: string;
  completed_at?: string;
  selected_section_ids?: string[];
  expires_at: string;
  user?: {
    full_name?: string;
    email?: string;
  };
}

export interface Question {
  id: string;
  section_id: string;
  text: string;
  type: string;
  weight: number;
  explanation: string;
  options: Array<{
    value: string;
    label: string;
    description?: string;
  }>;
}

export interface Section {
  id: string;
  title: string;
  description: string;
  questions: Question[];
}

export interface AssessmentStructure {
  sections: Section[];
}

export interface AssessmentResponse {
  id: string;
  assessment_id: string;
  question_id: string;
  answer_value: unknown;
  comment?: string;
  created_at: string;
  updated_at: string;
}

export interface Report {
  id: string;
  assessment_id: string;
  report_type: 'standard' | 'ai_enhanced';
  status: 'pending' | 'generating' | 'completed' | 'failed' | 'released';
  requested_at: string;
  completed_at?: string;
  file_path?: string;
  assessment?: {
    status?: string;
    attempt_number?: number;
    completed_at?: string;
  };
}

export interface Paginated<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface UserProgress {
  user_id: string;
  full_name: string;
  email: string;
  company_name: string;
  progress_percentage: number;
  assessment_status: string;
  days_since_activity: number;
}

export interface DashboardStats {
  total_users: number;
  active_users: number;
  total_assessments: number;
  completed_assessments: number;
  active_assessments: number;
  total_reports: number;
  pending_reports: number;
  new_users_this_week: number;
  expired_assessments: number;
  stuck_assessments: number;
  average_completion_hours: number;
}

export interface Alert {
  id: string;
  type: string;
  title: string;
  message: string;
  severity?: 'info' | 'warning' | 'error';
  created_at: string;
}

export interface ConsultationRequest {
  id: string;
  assessment_id: string;
  user_id: string;
  consultation_interest: boolean;
  consultation_details: string;
  created_at: string;
  user?: User;
  assessment?: Assessment;
  user_name: string;
  user_email: string;
  company_name: string;
}

export interface OpenAIKey {
  id: string;
  key_name: string;
  is_active: boolean;
  created_at: string;
  last_used_at: string | null;
  masked_key: string;
  usage_count: number;
  cooldown_until?: string;
  error_count: number;
  created_by?: string;
}

export interface Tier {
  id: string;
  name: string;
  description: string;
  section_ids: string[];
  duration: string;
  total_questions: number;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  detail?: string;
  message?: string;
}
