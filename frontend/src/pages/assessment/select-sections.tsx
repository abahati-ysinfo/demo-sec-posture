import { useState } from 'react';
import { useRouter } from 'next/router';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useAuth } from '@/lib/auth';
import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import { assessmentAPI } from '@/lib/api';
import toast from 'react-hot-toast';
import { CheckCircleIcon } from '@heroicons/react/24/outline';

interface Section {
  id: string;
  title: string;
  description: string;
  questions: unknown[];
}

const SECTION_DESCRIPTIONS: Record<string, string> = {
  section_1:
    'Evaluate your cybersecurity governance framework, strategic planning, policies, budget allocation, and board-level reporting mechanisms.',
  section_2:
    'Assess risk identification, analysis, treatment strategies, and business impact analysis processes.',
  section_3:
    'Review asset inventory management, classification schemes, lifecycle tracking, and data handling procedures.',
  section_4:
    'Examine directory services, access controls, user lifecycle management, and multi-factor authentication implementation.',
  section_5:
    'Analyze network architecture, segmentation, firewall configurations, monitoring capabilities, and remote access security.',
  section_6:
    'Evaluate endpoint protection platforms, mobile device management, and configuration management practices.',
  section_7:
    'Review data encryption standards, privacy compliance, backup strategies, and data governance frameworks.',
  section_8:
    'Assess secure development practices, web application security, API protection, and DevSecOps integration.',
  section_9:
    'Examine cloud infrastructure security, cloud IAM, container security, and serverless architecture protection.',
  section_10:
    'Evaluate incident response planning, detection capabilities, recovery procedures, and lessons learned processes.',
  section_11:
    'Review business continuity planning, disaster recovery capabilities, crisis management, and recovery operations.',
  section_12:
    'Assess vendor risk assessment processes, contract management, ongoing monitoring, and supply chain security.',
  section_13:
    'Evaluate security awareness programs, phishing defenses, role-based training, and compliance tracking.',
  section_14:
    'Review facility security controls, environmental protections, and equipment security measures.',
  section_15:
    'Assess security monitoring infrastructure, threat detection capabilities, and log management practices.',
  section_16:
    'Evaluate vulnerability assessment processes, management workflows, and patch management procedures.',
  section_17:
    'Review regulatory compliance status, internal audit processes, and external certification programs.',
  section_18:
    'Assess operational technology security, industrial control systems, and IoT device protection.',
  section_19:
    'Evaluate AI/ML model security, governance frameworks, and machine learning pipeline protection.',
};

export default function SelectSections() {
  const { user } = useAuth();
  const router = useRouter();
  const [selectedSections, setSelectedSections] = useState<Set<string>>(new Set());

  const { data: structure, isLoading: structureLoading } = useQuery({
    queryKey: ['assessmentStructure'],
    queryFn: assessmentAPI.getStructure,
  });

  const startAssessmentMutation = useMutation<unknown, Error, string[]>({
    mutationFn: (selectedSectionIds: string[]) =>
      assessmentAPI.startAssessmentWithSections(selectedSectionIds),
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

  const toggleSection = (sectionId: string) => {
    setSelectedSections((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(sectionId)) {
        newSet.delete(sectionId);
      } else {
        newSet.add(sectionId);
      }
      return newSet;
    });
  };

  const selectAll = () => {
    if (structure?.data?.sections) {
      setSelectedSections(new Set(structure.data.sections.map((s: Section) => s.id)));
    }
  };

  const clearAll = () => {
    setSelectedSections(new Set());
  };

  const handleStartAssessment = () => {
    if (selectedSections.size === 0) {
      toast.error('Please select at least one section');
      return;
    }

    startAssessmentMutation.mutate(Array.from(selectedSections));
  };

  const totalQuestions = structure?.data?.sections
    ? structure.data.sections
        .filter((s: Section) => selectedSections.has(s.id))
        .reduce((sum: number, s: Section) => sum + s.questions.length, 0)
    : 0;

  if (structureLoading) {
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

  return (
    <ProtectedRoute>
      <Layout title="Select Assessment Sections">
        <div className="max-w-5xl mx-auto py-8 px-4">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Customize Your Assessment</h1>
            <p className="text-gray-600 mb-6">
              Select the security domains you want to assess. You can choose as many or as few
              sections as needed for your evaluation.
            </p>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-lg font-semibold text-blue-900">
                    {selectedSections.size} sections selected
                  </p>
                  <p className="text-sm text-blue-700">{totalQuestions} total questions</p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={selectAll}
                    className="px-4 py-2 text-sm font-medium text-blue-700 bg-white border border-blue-300 rounded-md hover:bg-blue-50"
                  >
                    Select All
                  </button>
                  <button
                    onClick={clearAll}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                  >
                    Clear All
                  </button>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              {structure?.data?.sections.map((section: Section) => (
                <div
                  key={section.id}
                  className={`border rounded-lg p-4 cursor-pointer transition-all ${
                    selectedSections.has(section.id)
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                  onClick={() => toggleSection(section.id)}
                >
                  <div className="flex items-start">
                    <div className="flex-shrink-0 mt-1">
                      <div
                        className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                          selectedSections.has(section.id)
                            ? 'bg-primary-600 border-primary-600'
                            : 'border-gray-300 bg-white'
                        }`}
                      >
                        {selectedSections.has(section.id) && (
                          <CheckCircleIcon className="w-4 h-4 text-white" />
                        )}
                      </div>
                    </div>
                    <div className="ml-3 flex-1">
                      <div className="flex items-center justify-between">
                        <h3 className="text-lg font-semibold text-gray-900">{section.title}</h3>
                        <span className="text-sm text-gray-500 ml-2">
                          {section.questions.length} questions
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        {SECTION_DESCRIPTIONS[section.id] || section.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-8 flex justify-between items-center">
              <button
                onClick={() => router.push('/dashboard')}
                className="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleStartAssessment}
                disabled={selectedSections.size === 0 || startAssessmentMutation.isPending}
                className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                {startAssessmentMutation.isPending
                  ? 'Starting Assessment...'
                  : `Begin Assessment (${selectedSections.size} sections)`}
              </button>
            </div>
          </div>
        </div>
      </Layout>
    </ProtectedRoute>
  );
}
