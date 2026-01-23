import { useQuery } from '@tanstack/react-query';
import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import ErrorBoundary from '@/components/ErrorBoundary';
import { adminAPI } from '@/lib/api';
import {
  UserIcon,
  DocumentTextIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  ArrowTrendingUpIcon,
  KeyIcon,
} from '@heroicons/react/24/outline';
import Link from 'next/link';

export default function AdminDashboard() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboardStats'],
    queryFn: adminAPI.getDashboardStats,
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const { data: alerts, isLoading: alertsLoading } = useQuery({
    queryKey: ['adminAlerts'],
    queryFn: adminAPI.getAlerts,
    refetchInterval: 60000, // Refetch every minute
  });

  const { data: usersProgress, isLoading: usersProgressLoading } = useQuery({
    queryKey: ['usersProgress'],
    queryFn: adminAPI.getUsersProgressSummary,
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat().format(num);
  };

  return (
    <ProtectedRoute adminOnly>
      <Layout title="Admin Dashboard">
        <ErrorBoundary>
          <div className="max-w-7xl mx-auto">
            {/* Welcome Section */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Admin Dashboard</h2>
              <p className="text-gray-600">
                Monitor user activity, assessment progress, and system performance
              </p>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="card">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <UserIcon className="h-8 w-8 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Users</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {statsLoading ? '...' : formatNumber(stats?.data?.total_users || 0)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <DocumentTextIcon className="h-8 w-8 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Active Assessments</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {statsLoading ? '...' : formatNumber(stats?.data?.active_assessments || 0)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <ChartBarIcon className="h-8 w-8 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Completed</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {statsLoading ? '...' : formatNumber(stats?.data?.completed_assessments || 0)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <ArrowTrendingUpIcon className="h-8 w-8 text-indigo-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">New This Week</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {statsLoading ? '...' : formatNumber(stats?.data?.new_users_this_week || 0)}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Alerts Section */}
            {!alertsLoading && alerts?.data?.alerts && alerts.data.alerts.length > 0 && (
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">System Alerts</h3>
                <div className="space-y-4">
                  {alerts?.data?.alerts?.map(
                    (alert: { type: string; title: string; message: string }, index: number) => (
                      <div
                        key={index}
                        className={`p-4 rounded-lg border-l-4 ${
                          alert.type === 'warning'
                            ? 'bg-yellow-50 border-yellow-400'
                            : 'bg-blue-50 border-blue-400'
                        }`}
                      >
                        <div className="flex items-center">
                          <ExclamationTriangleIcon
                            className={`h-5 w-5 mr-3 ${
                              alert.type === 'warning' ? 'text-yellow-600' : 'text-blue-600'
                            }`}
                          />
                          <div>
                            <h4
                              className={`font-semibold ${
                                alert.type === 'warning' ? 'text-yellow-800' : 'text-blue-800'
                              }`}
                            >
                              {alert.title}
                            </h4>
                            <p
                              className={`text-sm ${
                                alert.type === 'warning' ? 'text-yellow-700' : 'text-blue-700'
                              }`}
                            >
                              {alert.message}
                            </p>
                          </div>
                        </div>
                      </div>
                    )
                  )}
                </div>
              </div>
            )}

            {/* Additional Stats */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Assessment Metrics</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Expired Assessments</span>
                    <span className="font-semibold text-red-600">
                      {statsLoading ? '...' : formatNumber(stats?.data?.expired_assessments || 0)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Stuck Assessments (7+ days)</span>
                    <span className="font-semibold text-orange-600">
                      {statsLoading ? '...' : formatNumber(stats?.data?.stuck_assessments || 0)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Average Completion Time</span>
                    <span className="font-semibold text-gray-900">
                      {statsLoading ? '...' : `${stats?.data?.average_completion_hours || 0}h`}
                    </span>
                  </div>
                </div>
              </div>

              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  <Link
                    href="/admin/users"
                    className="flex items-center p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                  >
                    <UserIcon className="h-6 w-6 text-primary-600 mr-3" />
                    <span>Manage Users</span>
                  </Link>
                  <Link
                    href="/admin/assessments"
                    className="flex items-center p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                  >
                    <DocumentTextIcon className="h-6 w-6 text-primary-600 mr-3" />
                    <span>View Assessments</span>
                  </Link>
                  <Link
                    href="/admin/reports"
                    className="flex items-center p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                  >
                    <ChartBarIcon className="h-6 w-6 text-primary-600 mr-3" />
                    <span>Manage Reports</span>
                  </Link>
                  <Link
                    href="/admin/openai-keys"
                    className="flex items-center p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                  >
                    <KeyIcon className="h-6 w-6 text-primary-600 mr-3" />
                    <span>Manage OpenAI Keys</span>
                  </Link>
                </div>
              </div>
            </div>

            {/* User Progress Tracking */}
            <div className="card mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">User Progress Overview</h3>
              {usersProgressLoading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                  <p className="text-gray-600 mt-2">Loading user progress...</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          User
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Company
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Progress
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Last Activity
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {usersProgress?.data?.users_progress
                        ?.slice(0, 10)
                        .map(
                          (user: {
                            user_id: string;
                            full_name: string;
                            email: string;
                            company_name: string;
                            progress_percentage: number;
                            assessment_status: string;
                            days_since_activity: number;
                          }) => (
                            <tr key={user.user_id}>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div className="text-sm font-medium text-gray-900">
                                  {user.full_name}
                                </div>
                                <div className="text-sm text-gray-500">{user.email}</div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                {user.company_name}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div className="flex items-center">
                                  <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                                    <div
                                      className="bg-primary-600 h-2 rounded-full"
                                      style={{ width: `${user.progress_percentage}%` }}
                                    ></div>
                                  </div>
                                  <span className="text-sm text-gray-900">
                                    {user.progress_percentage.toFixed(1)}%
                                  </span>
                                </div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <span
                                  className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                    user.assessment_status === 'completed'
                                      ? 'bg-green-100 text-green-800'
                                      : user.assessment_status === 'in_progress'
                                        ? 'bg-yellow-100 text-yellow-800'
                                        : 'bg-gray-100 text-gray-800'
                                  }`}
                                >
                                  {user.assessment_status.replace('_', ' ')}
                                </span>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {user.days_since_activity === 0
                                  ? 'Today'
                                  : `${user.days_since_activity} days ago`}
                              </td>
                            </tr>
                          )
                        )}
                    </tbody>
                  </table>
                  {usersProgress?.data?.users_progress &&
                    usersProgress.data.users_progress.length > 10 && (
                      <div className="mt-4 text-center">
                        <Link
                          href="/admin/users"
                          className="text-primary-600 hover:text-primary-500 text-sm font-medium"
                        >
                          View all {usersProgress?.data?.users_progress?.length || 0} users →
                        </Link>
                      </div>
                    )}
                </div>
              )}
            </div>

            {/* System Status */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <div className="w-3 h-3 bg-green-600 rounded-full"></div>
                  </div>
                  <p className="text-sm font-medium text-gray-900">API Status</p>
                  <p className="text-xs text-green-600">Operational</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <div className="w-3 h-3 bg-green-600 rounded-full"></div>
                  </div>
                  <p className="text-sm font-medium text-gray-900">Database</p>
                  <p className="text-xs text-green-600">Connected</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <div className="w-3 h-3 bg-green-600 rounded-full"></div>
                  </div>
                  <p className="text-sm font-medium text-gray-900">AI Service</p>
                  <p className="text-xs text-green-600">Available</p>
                </div>
              </div>
            </div>
          </div>
        </ErrorBoundary>
      </Layout>
    </ProtectedRoute>
  );
}
