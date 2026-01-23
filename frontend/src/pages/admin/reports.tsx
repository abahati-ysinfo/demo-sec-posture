import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Layout from '../../components/Layout';
import ProtectedRoute from '../../components/ProtectedRoute';
import ErrorBoundary from '../../components/ErrorBoundary';
import { adminAPI } from '../../lib/api';
import toast from 'react-hot-toast';
import { formatApiError } from '../../lib/formatApiError';
import {
  ChartBarIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  DocumentIcon,
  SparklesIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  PaperAirplaneIcon,
  ArrowDownTrayIcon,
} from '@heroicons/react/24/outline';

export default function AdminReports() {
  const [typeFilter, setTypeFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [downloadableOnly, setDownloadableOnly] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [downloadingReportId, setDownloadingReportId] = useState<string | null>(null);
  const limit = 20;
  const skip = (currentPage - 1) * limit;
  const queryClient = useQueryClient();

  const generateAIReportMutation = useMutation({
    mutationFn: (reportId: string) => adminAPI.generateAIReport(reportId),
    onSuccess: () => {
      toast.success('AI report generation started');
      queryClient.invalidateQueries({ queryKey: ['adminReports'] });
    },
    onError: (error: unknown) => {
      toast.error(formatApiError(error, 'Failed to generate AI report'));
    },
  });

  const releaseAIReportMutation = useMutation({
    mutationFn: (reportId: string) => adminAPI.releaseAIReport(reportId),
    onSuccess: () => {
      toast.success('AI report released to user');
      queryClient.invalidateQueries({ queryKey: ['adminReports'] });
    },
    onError: (error: unknown) => {
      toast.error(formatApiError(error, 'Failed to release AI report'));
    },
  });

  const retryStandardReportMutation = useMutation({
    mutationFn: (reportId: string) => adminAPI.retryStandardReport(reportId),
    onSuccess: () => {
      toast.success('Standard report retry started');
      queryClient.invalidateQueries({ queryKey: ['adminReports'] });
    },
    onError: (error: unknown) => {
      toast.error(formatApiError(error, 'Failed to retry standard report'));
    },
  });

  const handleDownloadReport = async (reportId: string, reportType: string) => {
    setDownloadingReportId(reportId);
    try {
      const response = await adminAPI.downloadReport(reportId);

      const contentDisposition = response.headers['content-disposition'];
      let filename = `security_assessment_report_${reportType}_${reportId}.pdf`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      if (typeof window !== 'undefined') {
        const blob = new Blob([response.data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      }

      toast.success('Report downloaded successfully');
    } catch (error: unknown) {
      toast.error(formatApiError(error, 'Failed to download report'));
    } finally {
      setDownloadingReportId(null);
    }
  };

  const isDownloadable = (status: string) => {
    return status === 'completed' || status === 'released';
  };

  const effectiveStatusFilter = downloadableOnly
    ? statusFilter || 'completed,released'
    : statusFilter;

  const {
    data: reportsData,
    isLoading,
    error,
  } = useQuery({
    queryKey: [
      'adminReports',
      { skip, limit, report_type: typeFilter, status: effectiveStatusFilter },
    ],
    queryFn: () =>
      adminAPI.getReports({
        skip,
        limit,
        report_type: typeFilter || undefined,
        status: effectiveStatusFilter || undefined,
      }),
    placeholderData: (previousData) => previousData,
    refetchInterval: 30000,
  });

  const reports = reportsData?.data?.items || [];
  const pagination = reportsData?.data;
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

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'ai_enhanced':
        return <SparklesIcon className="h-5 w-5 text-purple-600" />;
      case 'standard':
        return <DocumentIcon className="h-5 w-5 text-blue-600" />;
      default:
        return <ChartBarIcon className="h-5 w-5 text-gray-600" />;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-600" />;
      case 'pending':
        return <ClockIcon className="h-5 w-5 text-yellow-600" />;
      case 'failed':
        return <ExclamationTriangleIcon className="h-5 w-5 text-red-600" />;
      default:
        return <ChartBarIcon className="h-5 w-5 text-gray-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'ai_enhanced':
        return 'bg-purple-100 text-purple-800';
      case 'standard':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <ProtectedRoute adminOnly>
      <Layout title="Reports Management">
        <ErrorBoundary>
          <div className="max-w-7xl mx-auto">
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Reports Management</h2>
              <p className="text-gray-600">Monitor all generated reports and their status</p>
            </div>

            <div className="card mb-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <label
                    htmlFor="type-filter"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Filter by Type
                  </label>
                  <select
                    id="type-filter"
                    value={typeFilter}
                    onChange={(e) => {
                      setTypeFilter(e.target.value);
                      setCurrentPage(1);
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">All Types</option>
                    <option value="standard">Standard</option>
                    <option value="ai_enhanced">AI Enhanced</option>
                  </select>
                </div>
                <div>
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
                      setDownloadableOnly(false);
                      setCurrentPage(1);
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    disabled={downloadableOnly}
                  >
                    <option value="">All Statuses</option>
                    <option value="pending">Pending</option>
                    <option value="generating">Generating</option>
                    <option value="completed">Completed</option>
                    <option value="released">Released</option>
                    <option value="failed">Failed</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quick Filters
                  </label>
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={downloadableOnly}
                      onChange={(e) => {
                        setDownloadableOnly(e.target.checked);
                        if (e.target.checked) {
                          setStatusFilter('');
                        }
                        setCurrentPage(1);
                      }}
                      className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                    />
                    <span className="text-sm text-gray-700">Downloadable only</span>
                  </label>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  All Reports ({reports.length})
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
                  <p className="text-gray-600 mt-2">Loading reports...</p>
                </div>
              ) : error ? (
                <div className="text-center py-8">
                  <p className="text-red-600">Error loading reports. Please try again.</p>
                </div>
              ) : reports.length === 0 ? (
                <div className="text-center py-8">
                  <ChartBarIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">
                    {typeFilter || statusFilter
                      ? 'No reports found with the selected filters.'
                      : 'No reports found.'}
                  </p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">User</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Type</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Status</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">
                          Requested
                        </th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">
                          Completed
                        </th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {reports.map(
                        (report: {
                          id: string;
                          assessment_id: string;
                          report_type: string;
                          status: string;
                          requested_at: string;
                          completed_at?: string;
                          assessment?: {
                            user?: { full_name?: string; email?: string; company_name?: string };
                            status?: string;
                            attempt_number?: number;
                            completed_at?: string;
                          };
                        }) => (
                          <tr key={report.id} className="border-b border-gray-100 hover:bg-gray-50">
                            <td className="py-4 px-4">
                              <div>
                                <div className="font-medium text-gray-900">
                                  {report.assessment?.user?.full_name || 'Unknown User'}
                                </div>
                                <div className="text-sm text-gray-600">
                                  {report.assessment?.user?.email || 'No email'}
                                </div>
                                <div className="text-xs text-gray-500">
                                  {report.assessment?.user?.company_name || 'No company'}
                                </div>
                              </div>
                            </td>
                            <td className="py-4 px-4">
                              <div className="flex items-center gap-2">
                                {getTypeIcon(report.report_type)}
                                <span
                                  className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(report.report_type)}`}
                                >
                                  {report.report_type === 'ai_enhanced'
                                    ? 'AI Enhanced'
                                    : 'Standard'}
                                </span>
                              </div>
                            </td>
                            <td className="py-4 px-4">
                              <div className="flex items-center gap-2">
                                {getStatusIcon(report.status)}
                                <span
                                  className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(report.status)}`}
                                >
                                  {report.status.toUpperCase()}
                                </span>
                              </div>
                            </td>
                            <td className="py-4 px-4">
                              <span className="text-gray-600">
                                {formatDate(report.requested_at)}
                              </span>
                            </td>
                            <td className="py-4 px-4">
                              <span className="text-gray-600">
                                {report.completed_at ? formatDate(report.completed_at) : '-'}
                              </span>
                            </td>
                            <td className="py-4 px-4">
                              <div className="flex items-center gap-2 flex-wrap">
                                {isDownloadable(report.status) ? (
                                  <button
                                    onClick={() =>
                                      handleDownloadReport(report.id, report.report_type)
                                    }
                                    disabled={downloadingReportId === report.id}
                                    className="btn-primary text-xs flex items-center"
                                    title="Download report"
                                  >
                                    <ArrowDownTrayIcon className="h-3 w-3 mr-1" />
                                    {downloadingReportId === report.id
                                      ? 'Downloading...'
                                      : 'Download'}
                                  </button>
                                ) : (
                                  <button
                                    disabled
                                    className="btn-secondary text-xs flex items-center opacity-50 cursor-not-allowed"
                                    title={`Report must be completed or released to download (current: ${report.status})`}
                                  >
                                    <ArrowDownTrayIcon className="h-3 w-3 mr-1" />
                                    Download
                                  </button>
                                )}

                                {report.report_type === 'standard' &&
                                  report.status === 'failed' && (
                                    <button
                                      onClick={() => retryStandardReportMutation.mutate(report.id)}
                                      disabled={retryStandardReportMutation.isPending}
                                      className="btn-secondary text-xs flex items-center"
                                    >
                                      <ExclamationTriangleIcon className="h-3 w-3 mr-1" />
                                      {retryStandardReportMutation.isPending
                                        ? 'Retrying...'
                                        : 'Retry'}
                                    </button>
                                  )}
                                {report.report_type === 'ai_enhanced' &&
                                  report.status === 'pending' && (
                                    <button
                                      onClick={() => generateAIReportMutation.mutate(report.id)}
                                      disabled={generateAIReportMutation.isPending}
                                      className="btn-primary text-xs flex items-center"
                                    >
                                      <SparklesIcon className="h-3 w-3 mr-1" />
                                      {generateAIReportMutation.isPending
                                        ? 'Generating...'
                                        : 'Generate'}
                                    </button>
                                  )}
                                {report.report_type === 'ai_enhanced' &&
                                  report.status === 'completed' && (
                                    <button
                                      onClick={() => releaseAIReportMutation.mutate(report.id)}
                                      disabled={releaseAIReportMutation.isPending}
                                      className="btn-secondary text-xs flex items-center"
                                    >
                                      <PaperAirplaneIcon className="h-3 w-3 mr-1" />
                                      {releaseAIReportMutation.isPending
                                        ? 'Releasing...'
                                        : 'Release'}
                                    </button>
                                  )}
                              </div>
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
