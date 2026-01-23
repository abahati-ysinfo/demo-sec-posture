import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Layout from '../../components/Layout';
import ProtectedRoute from '../../components/ProtectedRoute';
import ErrorBoundary from '../../components/ErrorBoundary';
import { adminAPI } from '../../lib/api';
import {
  DocumentTextIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline';

export default function AdminAssessments() {
  const [statusFilter, setStatusFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const limit = 20;
  const skip = (currentPage - 1) * limit;

  const {
    data: assessmentsData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['adminAssessments', { skip, limit, status: statusFilter }],
    queryFn: () =>
      adminAPI.getAssessments({
        skip,
        limit,
        status: statusFilter || undefined,
      }),
    placeholderData: (previousData) => previousData,
    refetchInterval: 30000,
  });

  const assessments = assessmentsData?.data?.items || [];
  const pagination = assessmentsData?.data;
  const hasNextPage = pagination?.has_next || false;
  const hasPrevPage = pagination?.has_prev || false;

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-600" />;
      case 'in_progress':
        return <ClockIcon className="h-5 w-5 text-blue-600" />;
      case 'expired':
        return <ExclamationTriangleIcon className="h-5 w-5 text-red-600" />;
      default:
        return <DocumentTextIcon className="h-5 w-5 text-gray-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'expired':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getProgress = (progressPercentage: number) => {
    return Math.round(progressPercentage || 0);
  };

  return (
    <ProtectedRoute adminOnly>
      <Layout title="Assessments Management">
        <ErrorBoundary>
          <div className="max-w-7xl mx-auto">
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Assessments Management</h2>
              <p className="text-gray-600">Monitor all security assessments and their progress</p>
            </div>

            <div className="card mb-6">
              <div className="flex gap-4">
                <div className="flex-1">
                  <label
                    htmlFor="status-filter"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Filter by Status
                  </label>
                  <select
                    id="status-filter"
                    value={statusFilter}
                    onChange={(e) => {
                      setStatusFilter(e.target.value);
                      setCurrentPage(1);
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">All Statuses</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                    <option value="expired">Expired</option>
                  </select>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  All Assessments ({assessments.length})
                </h3>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
                    disabled={!hasPrevPage}
                    className="p-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                  >
                    <ChevronLeftIcon className="h-5 w-5" />
                  </button>
                  <span className="px-3 py-1 text-sm text-gray-600">Page {currentPage}</span>
                  <button
                    onClick={() => setCurrentPage((prev) => prev + 1)}
                    disabled={!hasNextPage}
                    className="p-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                  >
                    <ChevronRightIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>

              {isLoading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                  <p className="text-gray-600 mt-2">Loading assessments...</p>
                </div>
              ) : error ? (
                <div className="text-center py-8">
                  <p className="text-red-600">Error loading assessments. Please try again.</p>
                </div>
              ) : assessments.length === 0 ? (
                <div className="text-center py-8">
                  <DocumentTextIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">
                    {statusFilter
                      ? 'No assessments found with the selected status.'
                      : 'No assessments found.'}
                  </p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">User</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Status</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">
                          Progress
                        </th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Started</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Expires</th>
                      </tr>
                    </thead>
                    <tbody>
                      {assessments.map(
                        (assessment: {
                          id: string;
                          user?: { full_name?: string; email?: string };
                          status: string;
                          progress_percentage: number;
                          started_at: string;
                          expires_at: string;
                        }) => (
                          <tr
                            key={assessment.id}
                            className="border-b border-gray-100 hover:bg-gray-50"
                          >
                            <td className="py-4 px-4">
                              <div>
                                <div className="font-medium text-gray-900">
                                  {assessment.user?.full_name || 'Unknown User'}
                                </div>
                                <div className="text-sm text-gray-600">
                                  {assessment.user?.email || 'No email'}
                                </div>
                              </div>
                            </td>
                            <td className="py-4 px-4">
                              <div className="flex items-center gap-2">
                                {getStatusIcon(assessment.status)}
                                <span
                                  className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(assessment.status)}`}
                                >
                                  {assessment.status.replace('_', ' ').toUpperCase()}
                                </span>
                              </div>
                            </td>
                            <td className="py-4 px-4">
                              <div className="flex items-center gap-2">
                                <div className="w-24 bg-gray-200 rounded-full h-2">
                                  <div
                                    className="bg-primary-600 h-2 rounded-full"
                                    style={{
                                      width: `${getProgress(assessment.progress_percentage)}%`,
                                    }}
                                  ></div>
                                </div>
                                <span className="text-sm text-gray-600">
                                  {getProgress(assessment.progress_percentage)}%
                                </span>
                              </div>
                            </td>
                            <td className="py-4 px-4">
                              <span className="text-gray-600">
                                {formatDate(assessment.started_at)}
                              </span>
                            </td>
                            <td className="py-4 px-4">
                              <span
                                className={`text-sm ${
                                  new Date(assessment.expires_at) < new Date()
                                    ? 'text-red-600 font-medium'
                                    : 'text-gray-600'
                                }`}
                              >
                                {formatDate(assessment.expires_at)}
                              </span>
                            </td>
                          </tr>
                        )
                      )}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </ErrorBoundary>
      </Layout>
    </ProtectedRoute>
  );
}
