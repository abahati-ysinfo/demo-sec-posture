import React from 'react';
import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import { useAuth } from '@/lib/auth';
import Link from 'next/link';
import {
  DocumentTextIcon,
  CheckCircleIcon,
  ClockIcon,
  ArrowRightIcon,
} from '@heroicons/react/24/outline';

export default function AssessmentOverview() {
  const { user } = useAuth();

  return (
    <ProtectedRoute>
      <Layout title="Assessment Overview">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <CheckCircleIcon className="h-16 w-16 text-green-600 mx-auto mb-4" />
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Welcome to Your Security Assessment
            </h2>
            <p className="text-xl text-gray-600">Thank you for registering, {user?.full_name}!</p>
          </div>

          <div className="card mb-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">What to Expect</h3>
            <div className="space-y-4">
              <div className="flex items-start">
                <DocumentTextIcon className="h-6 w-6 text-primary-600 mt-1 mr-3" />
                <div>
                  <h4 className="font-semibold text-gray-900">Comprehensive Evaluation</h4>
                  <p className="text-gray-600">
                    Answer questions about your organization&apos;s security practices across
                    multiple domains.
                  </p>
                </div>
              </div>
              <div className="flex items-start">
                <ClockIcon className="h-6 w-6 text-primary-600 mt-1 mr-3" />
                <div>
                  <h4 className="font-semibold text-gray-900">15-Day Assessment Period</h4>
                  <p className="text-gray-600">
                    Take your time to provide accurate responses. Your progress is automatically
                    saved.
                  </p>
                </div>
              </div>
              <div className="flex items-start">
                <CheckCircleIcon className="h-6 w-6 text-primary-600 mt-1 mr-3" />
                <div>
                  <h4 className="font-semibold text-gray-900">AI-Enhanced Report</h4>
                  <p className="text-gray-600">
                    Receive personalized recommendations and actionable insights upon completion.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="text-center">
            <Link
              href="/assessment/start"
              className="btn-primary inline-flex items-center text-lg px-8 py-3"
            >
              Start Your Assessment
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
          </div>
        </div>
      </Layout>
    </ProtectedRoute>
  );
}
