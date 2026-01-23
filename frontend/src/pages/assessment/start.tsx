import { useState } from 'react';
import { useRouter } from 'next/router';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useAuth } from '@/lib/auth';
import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import { assessmentAPI } from '@/lib/api';
import toast from 'react-hot-toast';
import { ClockIcon, DocumentTextIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import IntakeWizard from '@/components/IntakeWizard';

export default function StartAssessment() {
  const { user } = useAuth();
  const router = useRouter();
  const [selectedTier, setSelectedTier] = useState<string>('standard');
  const [showAIWizard, setShowAIWizard] = useState<boolean>(false);

  const { data: tiersData, isLoading } = useQuery({
    queryKey: ['assessmentTiers'],
    queryFn: assessmentAPI.getTiers,
  });

  const startAssessmentMutation = useMutation<unknown, Error, string>({
    mutationFn: (tier: string) => assessmentAPI.startWithTier({ tier }),
    onSuccess: () => {
      toast.success('Assessment started!');
      router.push('/assessment/questions');
    },
    onError: (error: unknown) => {
      console.error('Failed to start assessment:', error);
      const errorMessage =
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
        'Failed to start assessment. Please try again.';
      toast.error(errorMessage);
    },
  });

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!user) {
    router.push('/auth/login');
    return null;
  }

  if (showAIWizard) {
    return (
      <ProtectedRoute>
        <IntakeWizard onBack={() => setShowAIWizard(false)} />
      </ProtectedRoute>
    );
  }

  const tiers = tiersData?.data?.tiers || {};
  const tierOrder = ['quick', 'standard', 'deep'];

  return (
    <ProtectedRoute>
      <Layout title="Start Assessment">
        <div className="max-w-6xl mx-auto py-8 px-4">
          <div className="bg-white rounded-lg shadow-md p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Choose Your Assessment Type</h1>
            <p className="text-gray-600 mb-8">
              Select the assessment level that best fits your needs. You can always customize
              sections later.
            </p>

            {/* AI-Guided Option Banner */}
            <div className="mb-8 bg-gradient-to-r from-primary-50 to-blue-50 border-2 border-primary-200 rounded-lg p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center mb-2">
                    <svg
                      className="w-6 h-6 text-primary-600 mr-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                      />
                    </svg>
                    <h3 className="text-xl font-bold text-gray-900">
                      Not sure which sections to choose?
                    </h3>
                    <span className="ml-3 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-600 text-white">
                      AI-Powered
                    </span>
                  </div>
                  <p className="text-gray-700 mb-4">
                    Answer a few quick questions about your role, environment, and goals. Our AI
                    will recommend the most relevant sections for you, saving you time and ensuring
                    you focus on what matters most.
                  </p>
                  <button onClick={() => setShowAIWizard(true)} className="btn-primary">
                    Get AI Recommendations
                  </button>
                </div>
              </div>
            </div>

            <div className="mb-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                Or choose a pre-defined tier:
              </h2>
            </div>

            <div className="grid md:grid-cols-3 gap-6 mb-8">
              {tierOrder.map((tierId) => {
                const tier = tiers[tierId];
                if (!tier) return null;

                const isSelected = selectedTier === tierId;
                const isQuick = tierId === 'quick';
                const isStandard = tierId === 'standard';
                const isDeep = tierId === 'deep';

                return (
                  <div
                    key={tierId}
                    className={`relative border-2 rounded-lg p-6 cursor-pointer transition-all ${
                      isSelected
                        ? 'border-primary-500 bg-primary-50 shadow-lg'
                        : 'border-gray-200 hover:border-gray-300 hover:shadow-md'
                    }`}
                    onClick={() => setSelectedTier(tierId)}
                  >
                    {isStandard && (
                      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                        <span className="bg-primary-600 text-white text-xs font-semibold px-3 py-1 rounded-full">
                          RECOMMENDED
                        </span>
                      </div>
                    )}

                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-xl font-bold text-gray-900">{tier.name}</h3>
                      <div
                        className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                          isSelected
                            ? 'bg-primary-600 border-primary-600'
                            : 'border-gray-300 bg-white'
                        }`}
                      >
                        {isSelected && <CheckCircleIcon className="w-4 h-4 text-white" />}
                      </div>
                    </div>

                    <p className="text-gray-600 mb-6 min-h-[3rem]">{tier.description}</p>

                    <div className="space-y-3">
                      <div className="flex items-center text-sm text-gray-700">
                        <ClockIcon className="w-5 h-5 mr-2 text-gray-400" />
                        <span>
                          <span className="font-medium">Duration:</span> {tier.duration}
                        </span>
                      </div>
                      <div className="flex items-center text-sm text-gray-700">
                        <DocumentTextIcon className="w-5 h-5 mr-2 text-gray-400" />
                        <span>
                          <span className="font-medium">Questions:</span> ~{tier.total_questions}
                        </span>
                      </div>
                    </div>

                    {isQuick && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <p className="text-xs text-gray-500">
                          Perfect for quick security checks and initial evaluations
                        </p>
                      </div>
                    )}
                    {isStandard && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <p className="text-xs text-gray-500">
                          Comprehensive evaluation covering all core security domains
                        </p>
                      </div>
                    )}
                    {isDeep && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <p className="text-xs text-gray-500">
                          Complete analysis including specialized areas like OT/ICS and AI/ML
                        </p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <p className="text-sm text-blue-900">
                <span className="font-semibold">Need more control?</span> You can also{' '}
                <button
                  onClick={() => router.push('/assessment/select-sections')}
                  className="text-blue-700 underline hover:text-blue-800"
                >
                  manually select specific sections
                </button>{' '}
                to customize your assessment.
              </p>
            </div>

            <div className="flex justify-between items-center">
              <button
                onClick={() => router.push('/dashboard')}
                className="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={() => startAssessmentMutation.mutate(selectedTier)}
                disabled={startAssessmentMutation.isPending}
                className="px-8 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed font-medium"
              >
                {startAssessmentMutation.isPending
                  ? 'Starting Assessment...'
                  : `Start ${tiers[selectedTier]?.name || 'Assessment'}`}
              </button>
            </div>
          </div>
        </div>
      </Layout>
    </ProtectedRoute>
  );
}
