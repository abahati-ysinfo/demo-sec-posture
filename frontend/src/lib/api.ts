import axios, { InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import Cookies from 'js-cookie';
import axiosRetry, { isNetworkError, isRetryableError } from 'axios-retry';
import type {
  User,
  Assessment,
  AssessmentStructure,
  AssessmentResponse,
  Report,
  Paginated,
  DashboardStats,
  Alert,
  ConsultationRequest,
  OpenAIKey,
  Tier,
  UserProgress,
} from './apiTypes';

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'https://security-posture-demo.fly.dev';

const ENABLE_CSRF = process.env.NEXT_PUBLIC_ENABLE_CSRF === 'true';

let csrfToken: string | null = null;
let authToken: string | null = null;

declare global {
  interface Window {
    __AUTH_TOKEN?: string;
    __setAuthToken?: (t: string | null) => void;
    __getAuthToken?: () => string | null;
  }
}

export const setCSRFToken = (token: string | null) => {
  csrfToken = token;
};

export const getCSRFToken = () => csrfToken;

export const setAuthToken = (token: string | null) => {
  authToken = token;

  if (typeof window !== 'undefined') {
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }
};

export const getAuthToken = () => authToken;

const E2E_MODE = process.env.NEXT_PUBLIC_E2E_MODE === 'true';
if (typeof window !== 'undefined' && E2E_MODE) {
  if (window.__AUTH_TOKEN && !authToken) {
    authToken = window.__AUTH_TOKEN;
  }
  window.__setAuthToken = (t: string | null) => {
    authToken = t;
  };
  window.__getAuthToken = () => authToken;
}

const pendingRequests = new Map<string, Promise<AxiosResponse>>();

function generateRequestKey(config: InternalAxiosRequestConfig): string {
  const { method, url, params, data } = config;
  return `${method}:${url}:${JSON.stringify(params)}:${JSON.stringify(data)}`;
}

function addPendingRequest(config: InternalAxiosRequestConfig, promise: Promise<AxiosResponse>) {
  const key = generateRequestKey(config);
  pendingRequests.set(key, promise);
  promise.finally(() => pendingRequests.delete(key));
}

function getPendingRequest(config: InternalAxiosRequestConfig): Promise<AxiosResponse> | undefined {
  const key = generateRequestKey(config);
  return pendingRequests.get(key);
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

axiosRetry(api, {
  retries: 3,
  retryDelay: (retryCount: number) => axiosRetry.exponentialDelay(retryCount, undefined, 500),
  retryCondition: (error: AxiosError) => isNetworkError(error) || isRetryableError(error),
  shouldResetTimeout: true,
});

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const pendingRequest = getPendingRequest(config);
  if (pendingRequest) {
    return Promise.reject({ _isDuplicate: true, promise: pendingRequest });
  }

  if (authToken && config.headers) {
    config.headers.Authorization = `Bearer ${authToken}`;
  }

  if (
    ENABLE_CSRF &&
    csrfToken &&
    config.method &&
    !['get', 'head', 'options'].includes(config.method.toLowerCase())
  ) {
    if (config.headers) {
      config.headers['X-CSRF-Token'] = csrfToken;
    }
  }

  return config;
});

api.interceptors.response.use(
  (response: AxiosResponse) => {
    if (response.config) {
      addPendingRequest(response.config as InternalAxiosRequestConfig, Promise.resolve(response));
    }
    return response;
  },
  (error: AxiosError | { _isDuplicate?: boolean; promise?: Promise<AxiosResponse> }) => {
    if ('_isDuplicate' in error && error._isDuplicate) {
      return error.promise;
    }

    if ('response' in error && error.response?.status === 401) {
      authToken = null;
      if (typeof window !== 'undefined') {
        Cookies.remove('access_token');
        window.location.href = '/auth/login';
      }
    }

    if ('config' in error && error.config) {
      addPendingRequest(error.config, Promise.reject(error));
    }

    return Promise.reject(error);
  }
);

export default api;

export const authAPI = {
  register: (data: { email: string; password: string; full_name: string; company_name: string }) =>
    api.post<{ access_token: string; user: User; csrf_token?: string }>('/api/auth/register', data),

  login: (data: { email: string; password: string }) =>
    api.post<{ access_token: string; user: User; csrf_token?: string }>('/api/auth/login', data),

  logout: () => api.post<{ message: string }>('/api/auth/logout'),

  getCurrentUser: () => api.get<User>('/api/auth/me'),

  getCSRFToken: () => api.get<{ csrf_token: string }>('/api/auth/csrf'),
};

export const assessmentAPI = {
  getStructure: () => api.get<AssessmentStructure>('/api/assessment/structure'),

  getFilteredStructure: (assessmentId: string) =>
    api.get<AssessmentStructure>(`/api/assessment/${assessmentId}/filtered-structure`),

  startAssessment: () => api.post<Assessment>('/api/assessment/start'),

  startAssessmentWithSections: (selectedSectionIds: string[]) =>
    api.post<Assessment>('/api/assessment/start', { selected_section_ids: selectedSectionIds }),

  getTiers: () => api.get<{ tiers: Record<string, Tier> }>('/api/assessment/tiers'),

  startWithTier: (data: { tier: string }) =>
    api.post<Assessment>('/api/assessment/start-with-tier', data),

  getCurrentAssessment: () => api.get<Assessment>('/api/assessment/current'),

  getLatestAssessment: () => api.get<Assessment>('/api/assessment/latest'),

  getAssessmentHistory: () => api.get<Assessment[]>('/api/assessment/history'),

  canRetakeAssessment: () =>
    api.get<{
      can_retake: boolean;
      message?: string;
      attempts_remaining?: number;
      total_attempts?: number;
    }>('/api/assessment/can-retake'),

  getResponses: (assessmentId: string) =>
    api.get<AssessmentResponse[]>(`/api/assessment/${assessmentId}/responses`),

  saveProgress: (assessmentId: string, responses: Record<string, unknown>[]) =>
    api.post<{ message: string; progress_percentage: number }>(
      `/api/assessment/${assessmentId}/save-progress`,
      { responses }
    ),

  completeAssessment: (assessmentId: string) =>
    api.post<{ message: string }>(`/api/assessment/${assessmentId}/complete`),

  saveConsultationInterest: (
    assessmentId: string,
    consultationData: { consultation_interest: boolean; consultation_details?: string }
  ) =>
    api.post<{ message: string }>(`/api/assessment/${assessmentId}/consultation`, consultationData),
};

export const reportsAPI = {
  generateReport: (assessmentId: string) =>
    api.post<Report>(`/api/reports/${assessmentId}/generate`),

  requestAIReport: (assessmentId: string, message?: string) =>
    api.post<Report>(`/api/reports/${assessmentId}/request-ai-report`, { message }),

  getUserReports: (params?: { skip?: number; limit?: number }) =>
    api.get<Paginated<Report>>('/api/reports/user/reports', { params }),

  getReportStatus: (reportId: string) => api.get<Report>(`/api/reports/${reportId}/status`),

  downloadReport: (reportId: string) =>
    api.get<Blob>(`/api/reports/${reportId}/download`, { responseType: 'blob' }),
};

export const adminAPI = {
  getUsers: (params?: {
    skip?: number;
    limit?: number;
    search?: string;
    sort_by?: string;
    sort_order?: string;
  }) => api.get<Paginated<User>>('/api/admin/users', { params }),

  getUser: (userId: string) => api.get<User>(`/api/admin/users/${userId}`),

  getUserAssessments: (userId: string) =>
    api.get<Assessment[]>(`/api/admin/users/${userId}/assessments`),

  getAssessments: (params?: { skip?: number; limit?: number; status?: string }) =>
    api.get<Paginated<Assessment>>('/api/admin/assessments', { params }),

  getDashboardStats: () => api.get<DashboardStats>('/api/admin/dashboard/stats'),

  getReports: (params?: { skip?: number; limit?: number; report_type?: string; status?: string }) =>
    api.get<Paginated<Report>>('/api/admin/reports', { params }),

  getAlerts: () => api.get<{ alerts: Alert[] }>('/api/admin/alerts'),
  getUsersProgressSummary: () =>
    api.get<{ users_progress: UserProgress[] }>('/api/admin/users-progress-summary'),
  generateAIReport: (reportId: string) =>
    api.post<{ message: string }>(`/api/reports/admin/${reportId}/generate-ai`),
  releaseAIReport: (reportId: string) =>
    api.post<{ message: string }>(`/api/reports/admin/${reportId}/release`),
  retryStandardReport: (reportId: string) =>
    api.post<{ message: string }>(`/api/reports/admin/${reportId}/retry-standard`),
  downloadReport: (reportId: string) =>
    api.get<Blob>(`/api/reports/${reportId}/download`, { responseType: 'blob' }),
  deleteUser: (userId: string) => api.delete<{ message: string }>(`/api/admin/users/${userId}`),
  resetUserPassword: (userId: string, newPassword: string) =>
    api.post<{ message: string }>(`/api/admin/users/${userId}/reset-password`, {
      new_password: newPassword,
    }),
  bulkUpdateUserStatus: (userIds: string[], isActive: boolean) =>
    api.post<{ message: string }>('/api/admin/users/bulk-update-status', {
      user_ids: userIds,
      is_active: isActive,
    }),
  bulkDeleteUsers: (userIds: string[]) =>
    api.post<{ message: string }>('/api/admin/users/bulk-delete', { user_ids: userIds }),

  getConsultationRequests: (skip = 0, limit = 100) => {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });
    return api.get<Paginated<ConsultationRequest>>(`/api/admin/consultations?${params}`);
  },

  listOpenAIKeys: (includeInactive = false) =>
    api.get<OpenAIKey[]>('/api/admin/openai-keys/', {
      params: { include_inactive: includeInactive },
    }),

  createOpenAIKey: (data: { key_name: string; api_key: string }) =>
    api.post<OpenAIKey>('/api/admin/openai-keys/', data),

  testOpenAIKey: (apiKey: string) =>
    api.post<{ success: boolean; message: string }>('/api/admin/openai-keys/test', {
      api_key: apiKey,
    }),

  toggleOpenAIKey: (keyId: string, isActive: boolean) =>
    api.patch<OpenAIKey>(`/api/admin/openai-keys/${keyId}/toggle`, { is_active: isActive }),

  deleteOpenAIKey: (keyId: string) =>
    api.delete<{ message: string }>(`/api/admin/openai-keys/${keyId}`),
};

export const intakeAPI = {
  getQuestions: () =>
    api.get<{
      questions: Array<{
        id: string;
        text: string;
        type: string;
        options?: Array<{ value: string; label: string }>;
        required: boolean;
      }>;
    }>('/api/intake/questions'),

  submitAndRecommend: (answers: {
    role: string;
    org_size: string;
    sector: string;
    environment: string;
    system_types: string[];
    cloud_providers: string[];
    primary_goal: string;
    primary_goal_detail?: string;
    time_preference: string;
  }) =>
    api.post<{
      recommended_sections: Array<{
        id: string;
        priority: string;
        reason: string;
        confidence?: number;
      }>;
      excluded_sections: Array<{
        id: string;
        reason: string;
        confidence?: number;
      }>;
      used_fallback: boolean;
      session_id: string;
    }>('/api/intake/recommend', { answers }),
};
