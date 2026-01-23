import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Layout from '../../components/Layout';
import ProtectedRoute from '../../components/ProtectedRoute';
import ErrorBoundary from '../../components/ErrorBoundary';
import { adminAPI } from '../../lib/api';
import {
  ChatBubbleLeftRightIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  EnvelopeIcon,
  BuildingOfficeIcon,
} from '@heroicons/react/24/outline';

export default function AdminConsultations() {
  const [currentPage, setCurrentPage] = useState(1);
  const limit = 20;
  const skip = (currentPage - 1) * limit;

  const {
    data: consultationsData,
    isLoading,
    error: _error,
  } = useQuery({
    queryKey: ['adminConsultations', { skip, limit }],
    queryFn: () => adminAPI.getConsultationRequests(skip, limit),
    placeholderData: (previousData) => previousData,
    refetchInterval: 30000,
  });

  const consultations = consultationsData?.data?.items || [];
  const pagination = consultationsData?.data;
  const hasNextPage = pagination?.has_next || false;
  const hasPrevPage = pagination?.has_prev || false;

  if (isLoading) {
    return (
      <ProtectedRoute adminOnly>
        <Layout title="Consultation Requests">
          <ErrorBoundary>
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600 mx-auto"></div>
              <p className="text-gray-600 mt-4">Loading consultation requests...</p>
            </div>
          </ErrorBoundary>
        </Layout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute adminOnly>
      <Layout title="Consultation Requests">
        <ErrorBoundary>
          <div className="max-w-7xl mx-auto">
            <div className="mb-8">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  Consultation Requests ({consultations.length})
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

              {consultations.length === 0 ? (
                <div className="text-center py-12">
                  <ChatBubbleLeftRightIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">No consultation requests yet</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {consultations.map(
                    (consultation: {
                      id: string;
                      user_name: string;
                      user_email: string;
                      company_name: string;
                      consultation_details: string;
                      created_at: string;
                    }) => (
                      <div key={consultation.id} className="card">
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center">
                            <ChatBubbleLeftRightIcon className="h-6 w-6 text-primary-600 mr-3" />
                            <div>
                              <h4 className="font-semibold text-gray-900">
                                {consultation.user_name}
                              </h4>
                              <div className="flex items-center text-sm text-gray-600 mt-1">
                                <EnvelopeIcon className="h-4 w-4 mr-1" />
                                {consultation.user_email}
                                <BuildingOfficeIcon className="h-4 w-4 ml-4 mr-1" />
                                {consultation.company_name}
                              </div>
                            </div>
                          </div>
                          <div className="text-sm text-gray-500">
                            {new Date(consultation.created_at).toLocaleDateString()}
                          </div>
                        </div>

                        <div className="bg-gray-50 rounded-lg p-4">
                          <h5 className="font-medium text-gray-900 mb-2">Consultation Details:</h5>
                          <p className="text-gray-700 whitespace-pre-wrap">
                            {consultation.consultation_details}
                          </p>
                        </div>

                        <div className="mt-4 flex justify-end">
                          <a
                            href={`mailto:${consultation.user_email}?subject=EchoStor Security Consultation&body=Hello ${consultation.user_name},%0D%0A%0D%0AThank you for your interest in our security consultation services.`}
                            className="btn-primary inline-flex items-center"
                          >
                            <EnvelopeIcon className="h-4 w-4 mr-2" />
                            Contact User
                          </a>
                        </div>
                      </div>
                    )
                  )}
                </div>
              )}
            </div>
          </div>
        </ErrorBoundary>
      </Layout>
    </ProtectedRoute>
  );
}
