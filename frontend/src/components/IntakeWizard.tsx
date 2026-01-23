import { useState } from 'react';
import { useRouter } from 'next/router';
import { useMutation, useQuery } from '@tanstack/react-query';
import { intakeAPI, assessmentAPI } from '@/lib/api';
import Layout from '@/components/Layout';
import toast from 'react-hot-toast';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline';

interface IntakeWizardProps {
  onBack: () => void;
}

interface IntakeAnswers {
  role: string;
  org_size: string;
  sector: string;
  environment: string;
  system_types: string[];
  cloud_providers: string[];
  primary_goal: string;
  primary_goal_detail?: string;
  time_preference: string;
}

interface SectionRecommendation {
  id: string;
  priority: string;
  reason: string;
  confidence?: number;
}

export default function IntakeWizard({ onBack }: IntakeWizardProps) {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Partial<IntakeAnswers>>({});
  const [recommendations, setRecommendations] = useState<SectionRecommendation[] | null>(null);
  const [selectedSections, setSelectedSections] = useState<Set<string>>(new Set());
  const [usedFallback, setUsedFallback] = useState(false);

  const { data: questionsData } = useQuery({
    queryKey: ['intakeQuestions'],
    queryFn: intakeAPI.getQuestions,
  });

  const { data: structureData } = useQuery({
    queryKey: ['assessmentStructure'],
    queryFn: assessmentAPI.getStructure,
  });

  const submitIntakeMutation = useMutation({
    mutationFn: (answers: IntakeAnswers) => intakeAPI.submitAndRecommend(answers),
    onSuccess: (response) => {
      setRecommendations(response.data.recommended_sections);
      setUsedFallback(response.data.used_fallback);

      const preSelected = new Set<string>();
      response.data.recommended_sections.forEach((rec) => {
        if (rec.priority === 'must_do') {
          preSelected.add(rec.id);
        } else if (rec.priority === 'should_do' && answers.time_preference !== 'quick') {
          preSelected.add(rec.id);
        }
      });
      setSelectedSections(preSelected);
      setCurrentStep(questions.length);
    },
    onError: (error) => {
      console.error('Failed to get recommendations:', error);
      toast.error('Failed to get recommendations. Please try again.');
    },
  });

  const startAssessmentMutation = useMutation({
    mutationFn: (sectionIds: string[]) => assessmentAPI.startAssessmentWithSections(sectionIds),
    onSuccess: () => {
      toast.success('Assessment started!');
      router.push('/assessment/questions');
    },
    onError: (error) => {
      console.error('Failed to start assessment:', error);
      toast.error('Failed to start assessment. Please try again.');
    },
  });

  const questions = questionsData?.data?.questions || [];
  const sections = structureData?.data?.sections || [];

  const currentQuestion = questions[currentStep];
  const isLastQuestion = currentStep === questions.length - 1;
  const isRecommendationsStep = currentStep === questions.length;

  const handleAnswerChange = (questionId: string, value: string | string[]) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }));
  };

  const handleNext = () => {
    if (!currentQuestion) return;

    const answer = answers[currentQuestion.id as keyof IntakeAnswers];
    if (currentQuestion.required && !answer) {
      toast.error('Please answer this question before continuing');
      return;
    }

    if (isLastQuestion) {
      submitIntakeMutation.mutate(answers as IntakeAnswers);
    } else {
      setCurrentStep((prev) => prev + 1);
    }
  };

  const handleBack = () => {
    if (currentStep === 0) {
      onBack();
    } else if (isRecommendationsStep) {
      setCurrentStep(questions.length - 1);
      setRecommendations(null);
    } else {
      setCurrentStep((prev) => prev - 1);
    }
  };

  const handleToggleSection = (sectionId: string) => {
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

  const handleStartAssessment = () => {
    if (selectedSections.size === 0) {
      toast.error('Please select at least one section');
      return;
    }
    startAssessmentMutation.mutate(Array.from(selectedSections));
  };

  const getSectionName = (sectionId: string) => {
    const section = sections.find((s: { id: string }) => s.id === sectionId);
    return section?.title || sectionId;
  };

  const getPriorityLabel = (priority: string) => {
    switch (priority) {
      case 'must_do':
        return 'Strongly Recommended';
      case 'should_do':
        return 'Recommended';
      case 'optional':
        return 'Optional';
      default:
        return priority;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'must_do':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'should_do':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'optional':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (isRecommendationsStep && recommendations) {
    const mustDo = recommendations.filter((r) => r.priority === 'must_do');
    const shouldDo = recommendations.filter((r) => r.priority === 'should_do');
    const optional = recommendations.filter((r) => r.priority === 'optional');

    return (
      <Layout title="AI Recommendations">
        <div className="max-w-4xl mx-auto py-8 px-4">
          <div className="bg-white rounded-lg shadow-md p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Your Personalized Assessment Plan
            </h1>
            <p className="text-gray-600 mb-6">
              Based on your answers, we&apos;ve selected the most relevant sections for you. You can
              adjust this selection before starting.
            </p>

            {usedFallback && (
              <div className="mb-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-sm text-yellow-800">
                  <strong>Note:</strong> We used our fallback recommendation system to generate
                  these suggestions. The recommendations are based on proven best practices for your
                  profile.
                </p>
              </div>
            )}

            <div className="space-y-6 mb-8">
              {mustDo.length > 0 && (
                <div>
                  <h2 className="text-xl font-bold text-gray-900 mb-4">
                    Strongly Recommended for You
                  </h2>
                  <div className="space-y-3">
                    {mustDo.map((rec) => (
                      <div
                        key={rec.id}
                        className="border-2 border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-all"
                      >
                        <div className="flex items-start">
                          <input
                            type="checkbox"
                            checked={selectedSections.has(rec.id)}
                            onChange={() => handleToggleSection(rec.id)}
                            className="mt-1 h-5 w-5 text-primary-600 rounded focus:ring-primary-500"
                          />
                          <div className="ml-4 flex-1">
                            <div className="flex items-center justify-between mb-2">
                              <h3 className="text-lg font-semibold text-gray-900">
                                {getSectionName(rec.id)}
                              </h3>
                              <span
                                className={`px-3 py-1 rounded-full text-xs font-medium border ${getPriorityColor(rec.priority)}`}
                              >
                                {getPriorityLabel(rec.priority)}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600">{rec.reason}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {shouldDo.length > 0 && (
                <div>
                  <h2 className="text-xl font-bold text-gray-900 mb-4">
                    Recommended If Time Allows
                  </h2>
                  <div className="space-y-3">
                    {shouldDo.map((rec) => (
                      <div
                        key={rec.id}
                        className="border-2 border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-all"
                      >
                        <div className="flex items-start">
                          <input
                            type="checkbox"
                            checked={selectedSections.has(rec.id)}
                            onChange={() => handleToggleSection(rec.id)}
                            className="mt-1 h-5 w-5 text-primary-600 rounded focus:ring-primary-500"
                          />
                          <div className="ml-4 flex-1">
                            <div className="flex items-center justify-between mb-2">
                              <h3 className="text-lg font-semibold text-gray-900">
                                {getSectionName(rec.id)}
                              </h3>
                              <span
                                className={`px-3 py-1 rounded-full text-xs font-medium border ${getPriorityColor(rec.priority)}`}
                              >
                                {getPriorityLabel(rec.priority)}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600">{rec.reason}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {optional.length > 0 && (
                <div>
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Optional Extras</h2>
                  <div className="space-y-3">
                    {optional.map((rec) => (
                      <div
                        key={rec.id}
                        className="border-2 border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-all"
                      >
                        <div className="flex items-start">
                          <input
                            type="checkbox"
                            checked={selectedSections.has(rec.id)}
                            onChange={() => handleToggleSection(rec.id)}
                            className="mt-1 h-5 w-5 text-primary-600 rounded focus:ring-primary-500"
                          />
                          <div className="ml-4 flex-1">
                            <div className="flex items-center justify-between mb-2">
                              <h3 className="text-lg font-semibold text-gray-900">
                                {getSectionName(rec.id)}
                              </h3>
                              <span
                                className={`px-3 py-1 rounded-full text-xs font-medium border ${getPriorityColor(rec.priority)}`}
                              >
                                {getPriorityLabel(rec.priority)}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600">{rec.reason}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <p className="text-sm text-blue-900">
                <strong>Selected:</strong> {selectedSections.size} section
                {selectedSections.size !== 1 ? 's' : ''}
              </p>
            </div>

            <div className="flex justify-between items-center">
              <button
                onClick={handleBack}
                className="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 flex items-center"
              >
                <ChevronLeftIcon className="w-5 h-5 mr-2" />
                Back
              </button>
              <button
                onClick={handleStartAssessment}
                disabled={startAssessmentMutation.isPending || selectedSections.size === 0}
                className="px-8 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed font-medium"
              >
                {startAssessmentMutation.isPending ? 'Starting Assessment...' : 'Start Assessment'}
              </button>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="AI Assessment Wizard">
      <div className="max-w-3xl mx-auto py-8 px-4">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <h1 className="text-2xl font-bold text-gray-900">AI Assessment Wizard</h1>
              <span className="text-sm text-gray-600">
                Question {currentStep + 1} of {questions.length}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-primary-600 h-2 rounded-full transition-all"
                style={{ width: `${((currentStep + 1) / questions.length) * 100}%` }}
              />
            </div>
          </div>

          {currentQuestion && (
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">{currentQuestion.text}</h2>

              {currentQuestion.type === 'single_select' && currentQuestion.options && (
                <div className="space-y-3">
                  {currentQuestion.options.map((option) => (
                    <label
                      key={option.value}
                      className="flex items-center p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-primary-300 transition-all"
                    >
                      <input
                        type="radio"
                        name={currentQuestion.id}
                        value={option.value}
                        checked={
                          answers[currentQuestion.id as keyof IntakeAnswers] === option.value
                        }
                        onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                        className="h-5 w-5 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="ml-3 text-gray-900">{option.label}</span>
                    </label>
                  ))}
                </div>
              )}

              {currentQuestion.type === 'multi_select' && currentQuestion.options && (
                <div className="space-y-3">
                  {currentQuestion.options.map((option) => (
                    <label
                      key={option.value}
                      className="flex items-center p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-primary-300 transition-all"
                    >
                      <input
                        type="checkbox"
                        value={option.value}
                        checked={(
                          (answers[currentQuestion.id as keyof IntakeAnswers] as string[]) || []
                        ).includes(option.value)}
                        onChange={(e) => {
                          const currentValues =
                            (answers[currentQuestion.id as keyof IntakeAnswers] as string[]) || [];
                          const newValues = e.target.checked
                            ? [...currentValues, option.value]
                            : currentValues.filter((v) => v !== option.value);
                          handleAnswerChange(currentQuestion.id, newValues);
                        }}
                        className="h-5 w-5 text-primary-600 rounded focus:ring-primary-500"
                      />
                      <span className="ml-3 text-gray-900">{option.label}</span>
                    </label>
                  ))}
                </div>
              )}
            </div>
          )}

          <div className="flex justify-between items-center">
            <button
              onClick={handleBack}
              className="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 flex items-center"
            >
              <ChevronLeftIcon className="w-5 h-5 mr-2" />
              {currentStep === 0 ? 'Cancel' : 'Back'}
            </button>
            <button
              onClick={handleNext}
              disabled={submitIntakeMutation.isPending}
              className="px-8 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed font-medium flex items-center"
            >
              {submitIntakeMutation.isPending ? (
                'Getting Recommendations...'
              ) : isLastQuestion ? (
                'Get Recommendations'
              ) : (
                <>
                  Next
                  <ChevronRightIcon className="w-5 h-5 ml-2" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
}
