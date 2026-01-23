import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import { useAuth } from '@/lib/auth';
import { assessmentAPI } from '@/lib/api';
import Link from 'next/link';
import {
  DocumentTextIcon,
  ChartBarIcon,
  ClockIcon,
  ArrowRightIcon,
  CheckCircleIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  InformationCircleIcon,
} from '@heroicons/react/24/outline';

export default function Dashboard() {
  const { user } = useAuth();
  const [showGuide, setShowGuide] = useState(false);

  const {
    data: assessment,
    isLoading: assessmentLoading,
    error: assessmentError,
  } = useQuery({
    queryKey: ['latestAssessment'],
    queryFn: assessmentAPI.getLatestAssessment,
    retry: false,
    refetchOnWindowFocus: false,
    refetchOnMount: 'always',
  });

  const { data: retakeData } = useQuery({
    queryKey: ['canRetake'],
    queryFn: assessmentAPI.canRetakeAssessment,
    refetchOnWindowFocus: false,
  });

  const calculateTimeRemaining = (expiresAt: string) => {
    const now = new Date();
    const expiry = new Date(expiresAt);
    const diffTime = expiry.getTime() - now.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays <= 0) return 'Expired';
    if (diffDays === 1) return '1 day';
    return `${diffDays} days`;
  };

  const hasActiveAssessment = assessment && !assessmentError;
  const isCompleted = hasActiveAssessment && assessment.data.status === 'completed';
  const progressPercentage = hasActiveAssessment ? assessment.data.progress_percentage || 0 : 0;
  const timeRemaining =
    hasActiveAssessment && !isCompleted && assessment.data.expires_at
      ? calculateTimeRemaining(assessment.data.expires_at)
      : null;

  const canRetake = retakeData?.data?.can_retake || false;
  const attemptsRemaining = retakeData?.data?.attempts_remaining || 0;
  const totalAttempts = retakeData?.data?.total_attempts || 0;

  return (
    <ProtectedRoute>
      <Layout title="Dashboard">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Welcome back, {user?.full_name}
            </h2>
            <p className="text-gray-600">
              Continue your security posture assessment for {user?.company_name}
            </p>
          </div>

          {!hasActiveAssessment && (
            <div className="card mb-8 bg-blue-50 border border-blue-200">
              <button
                onClick={() => setShowGuide(!showGuide)}
                className="w-full flex items-center justify-between text-left"
              >
                <div className="flex items-center">
                  <InformationCircleIcon className="h-6 w-6 text-blue-600 mr-3" />
                  <h3 className="text-lg font-semibold text-blue-900">How to Use This Tool</h3>
                </div>
                {showGuide ? (
                  <ChevronUpIcon className="h-5 w-5 text-blue-600" />
                ) : (
                  <ChevronDownIcon className="h-5 w-5 text-blue-600" />
                )}
              </button>

              {showGuide && (
                <div className="mt-4 pt-4 border-t border-blue-200 text-blue-900">
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-semibold mb-2">Overview</h4>
                      <p className="text-sm text-blue-800">
                        The Security Posture Assessment Tool helps you evaluate your
                        organization&apos;s cybersecurity maturity across 19 comprehensive security
                        domains. You can customize your assessment to focus on the areas most
                        relevant to your organization.
                      </p>
                    </div>

                    <div>
                      <h4 className="font-semibold mb-2">Step-by-Step Process</h4>
                      <ol className="list-decimal list-inside space-y-2 text-sm text-blue-800">
                        <li>
                          <strong>Select Sections:</strong> Choose which security domains you want
                          to assess (minimum 1 section required)
                        </li>
                        <li>
                          <strong>Answer Questions:</strong> Complete the assessment questions for
                          your selected sections
                        </li>
                        <li>
                          <strong>Auto-Save:</strong> Your progress is automatically saved every 10
                          minutes
                        </li>
                        <li>
                          <strong>Complete Assessment:</strong> Submit your assessment when finished
                        </li>
                        <li>
                          <strong>Get Reports:</strong> Receive your standard report immediately,
                          with optional AI-enhanced analysis available
                        </li>
                      </ol>
                    </div>

                    <div>
                      <h4 className="font-semibold mb-2">Tips for Success</h4>
                      <ul className="list-disc list-inside space-y-1 text-sm text-blue-800">
                        <li>You have 15 days to complete your assessment</li>
                        <li>Select only the sections relevant to your organization&apos;s needs</li>
                        <li>
                          Provide detailed comments where applicable for better recommendations
                        </li>
                        <li>You can save progress and return anytime within the 15-day window</li>
                        <li>Consider requesting the AI-enhanced report for deeper insights</li>
                      </ul>
                    </div>

                    <div className="bg-white rounded p-3 mt-4">
                      <p className="text-sm text-blue-900">
                        <strong>Ready to begin?</strong> Click &quot;Start Assessment&quot; below to
                        select your security domains and begin your evaluation.
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <Link
              href={
                isCompleted
                  ? '/reports'
                  : hasActiveAssessment
                    ? '/assessment/questions'
                    : '/assessment/start'
              }
              className="card hover:shadow-lg transition-shadow cursor-pointer"
            >
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <DocumentTextIcon className="h-8 w-8 text-primary-600" />
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {isCompleted
                      ? 'View Reports'
                      : hasActiveAssessment
                        ? 'Continue Assessment'
                        : 'Start Assessment'}
                  </h3>
                  <p className="text-gray-600">
                    {isCompleted
                      ? 'Download your completed reports'
                      : hasActiveAssessment
                        ? 'Resume your security evaluation'
                        : 'Begin your security evaluation'}
                  </p>
                </div>
                <ArrowRightIcon className="h-5 w-5 text-gray-400 ml-auto" />
              </div>
            </Link>

            <div className="card">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <ChartBarIcon className="h-8 w-8 text-green-600" />
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">Progress</h3>
                  <p className="text-gray-600">
                    {assessmentLoading
                      ? 'Loading...'
                      : `${progressPercentage.toFixed(1)}% Complete`}
                  </p>
                  {hasActiveAssessment && (
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                      <div
                        className="bg-green-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${progressPercentage}%` }}
                      ></div>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {!isCompleted && (
              <div className="card">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <ClockIcon className="h-8 w-8 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">Time Remaining</h3>
                    <p className="text-gray-600">
                      {assessmentLoading ? 'Loading...' : timeRemaining || '15 days'}
                    </p>
                  </div>
                </div>
              </div>
            )}
            {isCompleted && (
              <div className="card">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <CheckCircleIcon className="h-8 w-8 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">Status</h3>
                    <p className="text-gray-600">Assessment Completed</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {isCompleted
                ? 'Assessment Complete'
                : hasActiveAssessment
                  ? 'Your Assessment Progress'
                  : 'About Your Assessment'}
            </h3>
            <p className="text-gray-600 mb-4">
              {isCompleted
                ? `Congratulations! You have completed your security posture assessment with a score of ${progressPercentage.toFixed(1)}%. Your reports are ready for download.`
                : hasActiveAssessment
                  ? `You have completed ${progressPercentage.toFixed(1)}% of your security posture assessment. Continue where you left off to receive personalized recommendations and an AI-enhanced report.`
                  : 'Complete your comprehensive security posture assessment to receive personalized recommendations and an AI-enhanced report for your organization.'}
            </p>
            <Link
              href={
                isCompleted
                  ? '/reports'
                  : hasActiveAssessment
                    ? '/assessment/questions'
                    : '/assessment/start'
              }
              className="btn-primary inline-flex items-center"
            >
              {isCompleted
                ? 'View Reports'
                : hasActiveAssessment
                  ? 'Continue Assessment'
                  : 'Get Started'}
              <ArrowRightIcon className="ml-2 h-4 w-4" />
            </Link>
          </div>

          {isCompleted && canRetake && (
            <div className="card bg-blue-50 border border-blue-200 mt-6">
              <h3 className="text-lg font-semibold text-blue-900 mb-2">Retake Assessment</h3>
              <p className="text-blue-800 mb-4">
                You have completed {totalAttempts} of 3 possible assessments. You can retake the
                assessment {attemptsRemaining} more {attemptsRemaining === 1 ? 'time' : 'times'} to
                track your security posture improvements over time.
              </p>
              <Link href="/assessment/start" className="btn-primary inline-flex items-center">
                Retake Assessment
                <ArrowRightIcon className="ml-2 h-4 w-4" />
              </Link>
            </div>
          )}

          {isCompleted && !canRetake && totalAttempts >= 3 && (
            <div className="card bg-yellow-50 border border-yellow-200 mt-6">
              <h3 className="text-lg font-semibold text-yellow-900 mb-2">
                Assessment Limit Reached
              </h3>
              <p className="text-yellow-800">
                You have completed the maximum of 3 assessments. You can view all your previous
                reports in the Reports section.
              </p>
            </div>
          )}
        </div>
      </Layout>
    </ProtectedRoute>
  );
}
