/**
 * Centralized query keys for react-query
 * Ensures consistent cache key shapes across the application
 */

export const queryKeys = {
  currentUser: () => ['currentUser'] as const,

  assessmentStructure: (assessmentId?: string | null) =>
    assessmentId
      ? (['assessmentStructure', assessmentId] as const)
      : (['assessmentStructure'] as const),
  currentAssessment: () => ['currentAssessment'] as const,
  latestAssessment: () => ['latestAssessment'] as const,
  assessmentHistory: () => ['assessmentHistory'] as const,
  canRetakeAssessment: () => ['canRetakeAssessment'] as const,
  assessmentResponses: (assessmentId: string) => ['assessmentResponses', assessmentId] as const,
  assessmentTiers: () => ['assessmentTiers'] as const,

  userReports: (params?: { skip?: number; limit?: number }) =>
    params ? (['userReports', params] as const) : (['userReports'] as const),
  reportStatus: (reportId: string) => ['reportStatus', reportId] as const,

  adminUsers: (params?: { skip?: number; limit?: number; search?: string }) =>
    params ? (['adminUsers', params] as const) : (['adminUsers'] as const),
  adminUser: (userId: string) => ['adminUser', userId] as const,
  adminUserAssessments: (userId: string) => ['adminUserAssessments', userId] as const,
  adminAssessments: (params?: { skip?: number; limit?: number; status?: string }) =>
    params ? (['adminAssessments', params] as const) : (['adminAssessments'] as const),
  adminDashboardStats: () => ['adminDashboardStats'] as const,
  adminReports: (params?: {
    skip?: number;
    limit?: number;
    report_type?: string;
    status?: string;
  }) => (params ? (['adminReports', params] as const) : (['adminReports'] as const)),
  adminAlerts: () => ['adminAlerts'] as const,
  adminUsersProgressSummary: () => ['adminUsersProgressSummary'] as const,
  adminConsultationRequests: (skip?: number, limit?: number) =>
    ['adminConsultationRequests', { skip, limit }] as const,
  adminOpenAIKeys: (includeInactive?: boolean) => ['adminOpenAIKeys', { includeInactive }] as const,
} as const;
