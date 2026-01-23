import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Layout from '../components/Layout';
import ProtectedRoute from '../components/ProtectedRoute';
import Link from 'next/link';
import { reportsAPI } from '../lib/api';
import {
  ChartBarIcon,
  DocumentIcon,
  SparklesIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ArrowDownTrayIcon,
  PlusIcon,
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

export default function Reports() {
  const [_selectedReport, _setSelectedReport] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const {
    data: reportsData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['userReports'],
    queryFn: () => reportsAPI.getUserReports(),
    refetchInterval: 30000,
  });

  const downloadMutation = useMutation({
    mutationFn: (reportId: string) => reportsAPI.downloadReport(reportId),
    onSuccess: (response, reportId) => {
      if (typeof window !== 'undefined') {
        const blob = new Blob([response.data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `security_assessment_report_${reportId}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      }
      toast.success('Report downloaded successfully!');
    },
    onError: () => {
      toast.error('Failed to download report');
    },
  });

  const generateReportMutation = useMutation({
    mutationFn: (assessmentId: string) => reportsAPI.generateReport(assessmentId),
    onSuccess: () => {
      toast.success('Report generation started!');
      queryClient.invalidateQueries({ queryKey: ['userReports'] });
    },
    onError: () => {
      toast.error('Failed to generate report');
    },
  });

  const requestAIReportMutation = useMutation({
    mutationFn: (assessmentId: string) => reportsAPI.requestAIReport(assessmentId),
    onSuccess: () => {
      toast.success('AI-enhanced report requested! You will be notified when ready.');
      queryClient.invalidateQueries({ queryKey: ['userReports'] });
    },
    onError: () => {
      toast.error('Failed to request AI report');
    },
  });

  const reports = reportsData?.data?.items || [];

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

  const _getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-600" />;
      case 'pending':
        return <ClockIcon className="h-5 w-5 text-yellow-600" />;
      case 'generating':
        return <ClockIcon className="h-5 w-5 text-blue-600" />;
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
      case 'generating':
        return 'bg-blue-100 text-blue-800';
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

  const handleDownload = (reportId: string) => {
    downloadMutation.mutate(reportId);
  };

  const handleGenerateReport = (assessmentId: string) => {
    generateReportMutation.mutate(assessmentId);
  };

  const handleRequestAIReport = (assessmentId: string) => {
    requestAIReportMutation.mutate(assessmentId);
  };

  const completedAssessments = reports.filter(
    (report: {
      id: string;
      assessment_id: string;
      report_type: string;
      status: string;
      requested_at: string;
      completed_at?: string;
      assessment?: { status?: string; attempt_number?: number; completed_at?: string };
    }) => report.assessment?.status === 'completed'
  );

  const hasStandardReport = (assessmentId: string) => {
    return reports.some(
      (report: {
        id: string;
        assessment_id: string;
        report_type: string;
        status: string;
        requested_at: string;
        completed_at?: string;
        assessment?: { status?: string; attempt_number?: number; completed_at?: string };
      }) => report.assessment_id === assessmentId && report.report_type === 'standard'
    );
  };

  const hasAIReport = (assessmentId: string) => {
    return reports.some(
      (report: {
        id: string;
        assessment_id: string;
        report_type: string;
        status: string;
        requested_at: string;
        completed_at?: string;
        assessment?: { status?: string; attempt_number?: number; completed_at?: string };
      }) => report.assessment_id === assessmentId && report.report_type === 'ai_enhanced'
    );
  };

  return (
    <ProtectedRoute>
      <Layout title="My Reports">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              My Security Assessment Reports
            </h2>
            <p className="text-gray-600">
              Download your completed reports and request AI-enhanced analysis
            </p>
          </div>

          {isLoading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
              <p className="text-gray-600 mt-2">Loading your reports...</p>
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <ExclamationTriangleIcon className="h-12 w-12 text-red-400 mx-auto mb-4" />
              <p className="text-red-600">Error loading reports. Please try again.</p>
            </div>
          ) : reports.length === 0 ? (
            <div className="text-center py-12">
              <ChartBarIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No Reports Yet</h3>
              <p className="text-gray-600 mb-6">
                Complete a security assessment to generate your first report.
              </p>
              <Link href="/assessment/questions" className="btn-primary inline-flex items-center">
                <PlusIcon className="h-5 w-5 mr-2" />
                Start Assessment
              </Link>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Available Reports ({reports.length})
                </h3>

                <div className="space-y-4">
                  {reports.map(
                    (report: {
                      id: string;
                      assessment_id: string;
                      report_type: string;
                      status: string;
                      requested_at: string;
                      completed_at?: string;
                      assessment?: {
                        status?: string;
                        attempt_number?: number;
                        completed_at?: string;
                      };
                    }) => (
                      <div
                        key={report.id}
                        className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              {getTypeIcon(report.report_type)}
                              <span
                                className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(report.report_type)}`}
                              >
                                {report.report_type === 'ai_enhanced'
                                  ? 'AI Enhanced Report'
                                  : 'Standard Report'}
                              </span>
                              <span
                                className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(report.status)}`}
                              >
                                {report.status.toUpperCase()}
                              </span>
                            </div>

                            <div className="text-sm text-gray-600 space-y-1">
                              <p className="font-semibold text-gray-900">
                                Assessment #{report.assessment?.attempt_number || 1} -{' '}
                                {
                                  formatDate(
                                    report.assessment?.completed_at || report.requested_at
                                  ).split(',')[0]
                                }
                              </p>
                              <p>
                                Assessment completed:{' '}
                                {formatDate(report.assessment?.completed_at || report.requested_at)}
                              </p>
                              <p>Report requested: {formatDate(report.requested_at)}</p>
                              {report.completed_at && (
                                <p>Report completed: {formatDate(report.completed_at)}</p>
                              )}
                            </div>
                          </div>

                          <div className="flex items-center gap-2">
                            {(report.status === 'completed' || report.status === 'released') && (
                              <button
                                onClick={() => handleDownload(report.id)}
                                disabled={downloadMutation.isPending}
                                className="btn-secondary inline-flex items-center text-sm"
                              >
                                <ArrowDownTrayIcon className="h-4 w-4 mr-1" />
                                Download
                              </button>
                            )}

                            {report.status === 'generating' && (
                              <div className="flex items-center text-sm text-blue-600">
                                <ClockIcon className="h-4 w-4 mr-1" />
                                Generating...
                              </div>
                            )}

                            {report.status === 'pending' &&
                              report.report_type === 'ai_enhanced' && (
                                <span className="text-blue-600 text-sm">
                                  AI report requested - awaiting admin generation
                                </span>
                              )}

                            {report.status === 'completed' &&
                              report.report_type === 'ai_enhanced' && (
                                <span className="text-orange-600 text-sm">
                                  AI report generated - awaiting admin release
                                </span>
                              )}

                            {report.status === 'released' &&
                              report.report_type === 'ai_enhanced' && (
                                <span className="text-green-600 text-sm">
                                  AI report available for download
                                </span>
                              )}
                          </div>
                        </div>
                      </div>
                    )
                  )}
                </div>
              </div>

              {completedAssessments.length > 0 && (
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Generate Additional Reports
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Generate reports for your completed assessments that don&apos;t have reports
                    yet.
                  </p>

                  <div className="space-y-3">
                    {completedAssessments.map(
                      (report: {
                        id: string;
                        assessment_id: string;
                        report_type: string;
                        status: string;
                        requested_at: string;
                        completed_at?: string;
                        assessment?: {
                          status?: string;
                          attempt_number?: number;
                          completed_at?: string;
                        };
                      }) => {
                        const assessmentId = report.assessment_id;
                        const hasStandard = hasStandardReport(assessmentId);
                        const hasAI = hasAIReport(assessmentId);

                        if (hasStandard && hasAI) return null;

                        return (
                          <div
                            key={assessmentId}
                            className="flex items-center justify-between p-3 border border-gray-200 rounded-lg"
                          >
                            <div>
                              <p className="font-medium text-gray-900">
                                Assessment completed{' '}
                                {formatDate(report.assessment?.completed_at || '')}
                              </p>
                              <p className="text-sm text-gray-600">
                                {!hasStandard && !hasAI && 'No reports generated yet'}
                                {hasStandard && !hasAI && 'Standard report available'}
                                {!hasStandard && hasAI && 'AI report requested'}
                              </p>
                            </div>

                            <div className="flex gap-2">
                              {!hasStandard && (
                                <button
                                  onClick={() => handleGenerateReport(assessmentId)}
                                  disabled={generateReportMutation.isPending}
                                  className="btn-secondary text-sm"
                                >
                                  Generate Standard Report
                                </button>
                              )}

                              {!hasAI && (
                                <button
                                  onClick={() => handleRequestAIReport(assessmentId)}
                                  disabled={requestAIReportMutation.isPending}
                                  className="btn-primary text-sm inline-flex items-center"
                                >
                                  <SparklesIcon className="h-4 w-4 mr-1" />
                                  Request AI Report
                                </button>
                              )}
                            </div>
                          </div>
                        );
                      }
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </Layout>
    </ProtectedRoute>
  );
}
