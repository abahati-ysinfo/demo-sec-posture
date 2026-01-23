import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { useRouter } from 'next/router';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '@/lib/auth';
import { useAutoLogout } from '@/lib/useAutoLogout';
import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import ErrorBoundary from '@/components/ErrorBoundary';
import { assessmentAPI } from '@/lib/api';
import toast from 'react-hot-toast';
import { crossTabSync, SyncEventType } from '@/lib/crossTabSync';
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  BookmarkIcon,
  CheckCircleIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';

interface Question {
  id: string;
  section_id: string;
  text: string;
  type: string;
  weight: number;
  explanation: string;
  options: Array<{
    value: string;
    label: string;
    description?: string;
  }>;
}

interface Section {
  id: string;
  title: string;
  description: string;
  questions: Question[];
}

export default function AssessmentQuestions() {
  const { user } = useAuth();
  const router = useRouter();
  const queryClient = useQueryClient();
  const hasNavigatedToResumePoint = useRef(false);

  useAutoLogout(async () => {
    if (assessmentId) {
      await saveProgress();
    }
  });

  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [responses, setResponses] = useState<Record<string, unknown>>({});
  const [comments, setComments] = useState<Record<string, string>>({});
  const [consultationInterest, setConsultationInterest] = useState<boolean | null>(null);
  const [consultationDetails, setConsultationDetails] = useState<string>('');
  const [showConsultationQuestion, setShowConsultationQuestion] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [assessmentId, setAssessmentId] = useState<string | null>(null);
  const [savedProgress, setSavedProgress] = useState<number>(0);
  const [hasManuallyNavigated, setHasManuallyNavigated] = useState(false);
  const responsesRef = useRef(responses);

  const { data: structure, isLoading: structureLoading } = useQuery({
    queryKey: ['assessmentStructure', assessmentId],
    queryFn: () =>
      assessmentId
        ? assessmentAPI.getFilteredStructure(assessmentId)
        : assessmentAPI.getStructure(),
  });

  const {
    data: _assessment,
    isLoading: assessmentLoading,
    error: assessmentError,
  } = useQuery({
    queryKey: ['currentAssessment'],
    queryFn: assessmentAPI.getCurrentAssessment,
    retry: false,
  });

  useEffect(() => {
    if (_assessment?.data) {
      setAssessmentId(_assessment.data.id);
      setSavedProgress(_assessment.data.progress_percentage || 0);
      assessmentAPI.getResponses(_assessment.data.id).then((responseData) => {
        const existingResponses: Record<string, unknown> = {};
        const existingComments: Record<string, string> = {};
        responseData.data.forEach(
          (response: { question_id: string; answer_value: unknown; comment?: string }) => {
            existingResponses[response.question_id] = response.answer_value;
            if (response.comment) {
              existingComments[response.question_id] = response.comment;
            }
          }
        );
        setResponses((prev) => ({ ...prev, ...existingResponses }));
        setComments((prev) => ({ ...prev, ...existingComments }));
      });
    }
  }, [_assessment]);

  const startAssessmentMutation = useMutation({
    mutationFn: assessmentAPI.startAssessment,
    onSuccess: (data) => {
      setAssessmentId(data.data.id);
      queryClient.invalidateQueries({ queryKey: ['currentAssessment'] });
      queryClient.invalidateQueries({ queryKey: ['latestAssessment'] });
      crossTabSync.broadcast(SyncEventType.ASSESSMENT_STARTED, data.data.id);
    },
    onError: (error: unknown) => {
      console.error('Failed to start assessment:', error);
      const errorMessage =
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
        'Failed to start assessment. Please try again.';
      toast.error(errorMessage);
    },
  });

  const saveProgressMutation = useMutation({
    mutationFn: ({
      assessmentId,
      responses,
    }: {
      assessmentId: string;
      responses: Record<string, unknown>[];
    }) => assessmentAPI.saveProgress(assessmentId, responses),
    onSuccess: (data, variables) => {
      setLastSaved(new Date());
      if (data.data.progress_percentage !== undefined) {
        setSavedProgress(data.data.progress_percentage);
      }

      queryClient.invalidateQueries({ queryKey: ['currentAssessment'] });
      queryClient.invalidateQueries({ queryKey: ['latestAssessment'] });

      queryClient.setQueryData(['latestAssessment'], (oldData: unknown) => {
        if (oldData && typeof oldData === 'object' && 'data' in oldData) {
          const typedData = oldData as { data: Record<string, unknown> };
          return {
            ...typedData,
            data: {
              ...typedData.data,
              progress_percentage: data.data.progress_percentage,
              last_saved_at: new Date().toISOString(),
            },
          };
        }
        return oldData;
      });

      crossTabSync.broadcast(SyncEventType.PROGRESS_SAVED, variables.assessmentId);
      toast.success('Progress saved!');
    },
    onError: (_error: unknown) => {
      toast.error('Failed to save progress');
    },
  });

  const completeAssessmentMutation = useMutation({
    mutationFn: (assessmentId: string) => assessmentAPI.completeAssessment(assessmentId),
    onSuccess: (_data, assessmentId) => {
      crossTabSync.broadcast(SyncEventType.ASSESSMENT_COMPLETED, assessmentId);
      toast.success('Assessment completed!');
      router.push('/reports');
    },
    onError: (_error: unknown) => {
      toast.error('Failed to complete assessment');
    },
  });

  useEffect(() => {
    responsesRef.current = responses;
  }, [responses]);

  useEffect(() => {
    if (!assessmentId) return;

    const interval = setInterval(
      () => {
        const currentResponses = responsesRef.current;
        if (Object.keys(currentResponses).length > 0) {
          const responseArray = Object.entries(currentResponses).map(([questionId, value]) => {
            const question = findQuestionById(questionId);
            return {
              section_id: question?.section_id || '',
              question_id: questionId,
              answer_value: value,
              comment: comments[questionId] || null,
            };
          });

          saveProgressMutation.mutate({ assessmentId, responses: responseArray });
        }
      },
      10 * 60 * 1000
    );

    return () => clearInterval(interval);
  }, [assessmentId]);

  useEffect(() => {
    if (!structure || !responses || hasNavigatedToResumePoint.current) return;
    if (Object.keys(responses).length === 0) return;
    if (hasManuallyNavigated) return;
    if (savedProgress <= 0) return;

    const { sectionIndex, questionIndex, allAnswered } = findFirstUnansweredQuestion();
    setCurrentSectionIndex(sectionIndex);
    setCurrentQuestionIndex(questionIndex);
    if (allAnswered) {
      setShowConsultationQuestion(true);
    }
    hasNavigatedToResumePoint.current = true;
  }, [structure, responses, hasManuallyNavigated, savedProgress]);

  useEffect(() => {
    setHasManuallyNavigated(false);
    hasNavigatedToResumePoint.current = false;
  }, [assessmentId]);

  useEffect(() => {
    const currentTabId = crossTabSync.getTabId();
    const unsubscribe = crossTabSync.subscribe((event) => {
      if (event.assessmentId !== assessmentId && assessmentId) return;

      if (event.originTabId === currentTabId) return;

      switch (event.type) {
        case SyncEventType.ASSESSMENT_STARTED:
        case SyncEventType.PROGRESS_SAVED:
          queryClient.invalidateQueries({ queryKey: ['currentAssessment'] });
          queryClient.invalidateQueries({ queryKey: ['latestAssessment'] });
          toast('Assessment updated in another tab', { icon: '🔄' });
          break;
        case SyncEventType.ASSESSMENT_COMPLETED:
          queryClient.invalidateQueries({ queryKey: ['currentAssessment'] });
          queryClient.invalidateQueries({ queryKey: ['latestAssessment'] });
          toast.success('Assessment completed in another tab');
          router.push('/reports');
          break;
      }
    });

    return () => {
      unsubscribe();
    };
  }, [assessmentId, queryClient, router]);

  const saveProgress = () => {
    if (!assessmentId || !structure) return;

    const responseArray = Object.entries(responses).map(([questionId, value]) => {
      const question = findQuestionById(questionId);
      return {
        section_id: question?.section_id || '',
        question_id: questionId,
        answer_value: value,
        comment: comments[questionId] || null,
      };
    });

    saveProgressMutation.mutate({ assessmentId, responses: responseArray });
  };

  const handleCommentChange = (questionId: string, comment: string) => {
    const wordCount = comment
      .trim()
      .split(/\s+/)
      .filter((word) => word.length > 0).length;
    if (wordCount <= 150) {
      setComments((prev) => ({
        ...prev,
        [questionId]: comment,
      }));
    }
  };

  const findQuestionById = (questionId: string): Question | undefined => {
    if (!structure) return undefined;

    for (const section of structure.data.sections) {
      const question = section.questions.find((q: Question) => q.id === questionId);
      if (question) return question;
    }
    return undefined;
  };

  const findFirstUnansweredQuestion = (): {
    sectionIndex: number;
    questionIndex: number;
    allAnswered: boolean;
  } => {
    if (!structure) return { sectionIndex: 0, questionIndex: 0, allAnswered: false };

    for (let sectionIndex = 0; sectionIndex < structure.data.sections.length; sectionIndex++) {
      const section = structure.data.sections[sectionIndex];
      for (let questionIndex = 0; questionIndex < section.questions.length; questionIndex++) {
        const question = section.questions[questionIndex];
        if (!responses[question.id]) {
          return { sectionIndex, questionIndex, allAnswered: false };
        }
      }
    }
    const lastSectionIndex = structure.data.sections.length - 1;
    const lastSection = structure.data.sections[lastSectionIndex];
    const lastQuestionIndex = lastSection.questions.length - 1;
    return { sectionIndex: lastSectionIndex, questionIndex: lastQuestionIndex, allAnswered: true };
  };

  const handleAnswerChange = useCallback((questionId: string, value: unknown) => {
    setResponses((prev) => ({
      ...prev,
      [questionId]: value,
    }));
  }, []);

  const isQuestionAnswered = (question: Question): boolean => {
    const answer = responses[question.id];

    if (question.type === 'multiple_select') {
      return Array.isArray(answer) && answer.length > 0;
    }

    return answer !== undefined && answer !== null && answer !== '';
  };

  const isCurrentQuestionAnswered = (): boolean => {
    if (!currentQuestion) return false;
    return isQuestionAnswered(currentQuestion);
  };

  const getCurrentQuestion = (): Question | null => {
    if (!structure || !structure.data.sections[currentSectionIndex]) return null;
    const section = structure.data.sections[currentSectionIndex];
    return section.questions[currentQuestionIndex] || null;
  };

  const getCurrentSection = (): Section | null => {
    if (!structure || !structure.data.sections[currentSectionIndex]) return null;
    return structure.data.sections[currentSectionIndex];
  };

  const goToNextQuestion = async () => {
    const section = getCurrentSection();
    if (!section) return;

    if (currentQuestionIndex < section.questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    } else if (currentSectionIndex < (structure?.data?.sections?.length || 0) - 1) {
      if (!assessmentId || !structure) return;

      const responseArray = Object.entries(responses).map(([questionId, value]) => {
        const question = findQuestionById(questionId);
        return {
          section_id: question?.section_id || '',
          question_id: questionId,
          answer_value: value,
          comment: comments[questionId] || null,
        };
      });

      try {
        await saveProgressMutation.mutateAsync({ assessmentId, responses: responseArray });
        setCurrentSectionIndex((prev) => prev + 1);
        setCurrentQuestionIndex(0);
      } catch {
        toast.error('Failed to save progress. Please try again.');
      }
    } else if (!showConsultationQuestion) {
      saveProgress();
      setShowConsultationQuestion(true);
    }
  };

  const goToPreviousQuestion = () => {
    if (showConsultationQuestion) {
      setShowConsultationQuestion(false);
      return;
    }
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    } else if (currentSectionIndex > 0) {
      setCurrentSectionIndex((prev) => prev - 1);
      const prevSection = structure?.data?.sections?.[currentSectionIndex - 1];
      if (prevSection) {
        setCurrentQuestionIndex(prevSection.questions.length - 1);
      }
    }
  };

  const isLastQuestion = () => {
    if (!structure) return false;
    const isLastAssessmentQuestion =
      currentSectionIndex === structure.data.sections.length - 1 &&
      currentQuestionIndex === structure.data.sections[currentSectionIndex].questions.length - 1;

    if (isLastAssessmentQuestion && !showConsultationQuestion) {
      return false;
    }
    return showConsultationQuestion;
  };

  const handleCompleteAssessment = async () => {
    if (!assessmentId) return;

    if (
      confirm(
        'Are you sure you want to complete the assessment? You won&apos;t be able to make changes after this.'
      )
    ) {
      try {
        if (consultationInterest !== null) {
          const consultationData = {
            consultation_interest: consultationInterest,
            consultation_details: consultationInterest ? consultationDetails : undefined,
          };
          await assessmentAPI.saveConsultationInterest(assessmentId, consultationData);
        }

        saveProgress();
        setTimeout(() => {
          completeAssessmentMutation.mutate(assessmentId);
        }, 1000);
      } catch (error) {
        console.error('Failed to save consultation data:', error);
      }
    }
  };

  useEffect(() => {
    if (!user) {
      router.push('/auth/login');
    }
  }, [user, router]);

  const {
    percentage: progress,
    answeredCount,
    totalQuestions,
  } = useMemo(() => {
    if (!structure) return { percentage: 0, answeredCount: 0, totalQuestions: 0 };

    let answered = 0;
    let total = 0;

    structure.data.sections.forEach((section: Section) => {
      total += section.questions.length;
      section.questions.forEach((question: Question) => {
        if (isQuestionAnswered(question)) {
          answered++;
        }
      });
    });

    const percentage = total > 0 ? (answered / total) * 100 : 0;
    return { percentage, answeredCount: answered, totalQuestions: total };
  }, [structure, responses]);

  if (structureLoading || (assessmentLoading && !assessmentError)) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (startAssessmentMutation.isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Starting your assessment...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  if (assessmentError && !assessmentId && startAssessmentMutation.isError) {
    return (
      <Layout title="Assessment Questions">
        <div className="max-w-2xl mx-auto text-center py-12">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-red-800 mb-2">Unable to Start Assessment</h3>
            <p className="text-red-700 mb-4">
              We encountered an issue while trying to start your security assessment. This could be
              due to a temporary server issue or authentication problem.
            </p>
            <button
              onClick={() => {
                startAssessmentMutation.reset();
                startAssessmentMutation.mutate();
              }}
              disabled={startAssessmentMutation.isPending}
              className="btn-primary mr-4"
              data-testid="retry-start-assessment"
            >
              {startAssessmentMutation.isPending ? 'Starting...' : 'Try Again'}
            </button>
            <button
              onClick={() => router.push('/dashboard')}
              className="btn-secondary"
              data-testid="return-to-dashboard"
            >
              Return to Dashboard
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  if (assessmentError && !assessmentId && !startAssessmentMutation.isError) {
    return (
      <Layout title="Assessment Questions">
        <div className="max-w-2xl mx-auto text-center py-12">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-blue-800 mb-2">
              Ready to Start Your Assessment?
            </h3>
            <p className="text-blue-700 mb-4">
              No active assessment was found. Click below to begin your comprehensive security
              posture evaluation.
            </p>
            <button
              onClick={() => startAssessmentMutation.mutate()}
              disabled={startAssessmentMutation.isPending}
              className="btn-primary"
              data-testid="start-new-assessment"
            >
              {startAssessmentMutation.isPending ? 'Starting...' : 'Start Assessment'}
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  const currentQuestion = getCurrentQuestion();
  const currentSection = getCurrentSection();

  const calculateSectionProgress = (sectionIndex: number) => {
    if (!structure) return 0;
    const section = structure.data.sections[sectionIndex];
    const answeredInSection = section.questions.filter((q: Question) =>
      isQuestionAnswered(q)
    ).length;
    return (answeredInSection / section.questions.length) * 100;
  };

  const goToSection = (sectionIndex: number) => {
    setHasManuallyNavigated(true);
    setCurrentSectionIndex(sectionIndex);
    setCurrentQuestionIndex(0);
    setShowConsultationQuestion(false);
  };

  if (!currentQuestion || !currentSection) {
    return (
      <Layout title="Assessment Questions">
        <div className="max-w-2xl mx-auto text-center py-12">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-yellow-800 mb-2">
              Assessment Structure Loading
            </h3>
            <p className="text-yellow-700 mb-4">
              We&apos;re having trouble loading the assessment questions. Please try refreshing the
              page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="btn-primary mr-4"
              data-testid="refresh-page"
            >
              Refresh Page
            </button>
            <button
              onClick={() => router.push('/dashboard')}
              className="btn-secondary"
              data-testid="return-to-dashboard-fallback"
            >
              Return to Dashboard
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <ProtectedRoute>
      <Layout title="Security Assessment">
        <ErrorBoundary>
          <div className="flex gap-6 max-w-7xl mx-auto">
            {/* Left Sidebar - Section Progress */}
            <div className="hidden lg:block w-64 flex-shrink-0">
              <div className="sticky top-4 bg-white rounded-lg shadow-md p-4 max-h-[calc(100vh-2rem)] overflow-y-auto">
                <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                  <svg
                    className="h-4 w-4 mr-2 text-primary-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  Assessment Sections
                </h3>

                {/* Overall Progress */}
                <div className="mb-4 pb-4 border-b border-gray-200">
                  <div className="text-xs font-medium text-gray-700 mb-1">Overall Progress</div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mb-1">
                    <div
                      className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                  <div className="text-xs text-gray-600">{Math.round(progress)}% Complete</div>
                </div>

                {/* Section List */}
                <div className="space-y-2">
                  {structure?.data?.sections.map((section: Section, index: number) => {
                    const sectionProgress = calculateSectionProgress(index);
                    const isCurrentSection = index === currentSectionIndex;
                    const answeredCount = section.questions.filter((q: Question) =>
                      isQuestionAnswered(q)
                    ).length;

                    return (
                      <button
                        key={section.id}
                        onClick={() => goToSection(index)}
                        className={`w-full text-left p-3 rounded-lg transition-all ${
                          isCurrentSection
                            ? 'bg-primary-50 border-2 border-primary-500'
                            : 'bg-gray-50 border border-gray-200 hover:bg-gray-100'
                        }`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex-1 min-w-0">
                            <div
                              className={`text-xs font-medium truncate ${
                                isCurrentSection ? 'text-primary-900' : 'text-gray-900'
                              }`}
                            >
                              {section.title}
                            </div>
                            <div className="text-xs text-gray-600 mt-0.5">
                              {answeredCount}/{section.questions.length}
                            </div>
                          </div>
                          {sectionProgress === 100 && (
                            <svg
                              className="h-4 w-4 text-green-500 flex-shrink-0 ml-2"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
                              <path
                                fillRule="evenodd"
                                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                clipRule="evenodd"
                              />
                            </svg>
                          )}
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-1.5">
                          <div
                            className={`h-1.5 rounded-full transition-all duration-300 ${
                              sectionProgress === 100 ? 'bg-green-500' : 'bg-primary-500'
                            }`}
                            style={{ width: `${sectionProgress}%` }}
                          ></div>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 min-w-0">
              {/* Enhanced Progress Bar */}
              <div className="mb-8">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700">
                    Assessment Progress: {progress.toFixed(0)}% ({answeredCount} of {totalQuestions}{' '}
                    questions)
                  </span>
                  <div className="flex items-center text-sm text-gray-600">
                    <ClockIcon className="h-4 w-4 mr-1" />
                    {lastSaved ? `Auto-saved ${lastSaved.toLocaleTimeString()}` : 'Not saved yet'}
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-gradient-to-r from-primary-500 to-primary-600 h-3 rounded-full transition-all duration-500 relative"
                    style={{ width: `${progress}%` }}
                  >
                    <div className="absolute right-0 top-0 h-3 w-1 bg-primary-700 rounded-r-full"></div>
                  </div>
                </div>
                <div className="mt-1 text-xs text-gray-500">
                  Section {currentSectionIndex + 1} of {structure?.data?.sections?.length || 0}:{' '}
                  {currentSection?.title}
                </div>
              </div>

              {/* Section Info */}
              <div className="bg-primary-50 rounded-lg p-4 mb-6">
                <h2 className="text-lg font-semibold text-primary-900 mb-2">
                  {currentSection.title}
                </h2>
                <p className="text-primary-700 text-sm">{currentSection.description}</p>
                <div className="mt-2 text-sm text-primary-600">
                  Question {currentQuestionIndex + 1} of {currentSection.questions.length} in this
                  section
                </div>
              </div>

              {/* Question */}
              <div className="card mb-6">
                <div className="mb-4">
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="text-lg font-semibold text-gray-900 flex-1">
                      {currentQuestion.text}
                    </h3>
                    <div className="ml-4 px-2 py-1 bg-gray-100 rounded text-sm font-medium text-gray-600">
                      Weight: {currentQuestion.weight}
                    </div>
                  </div>

                  {currentQuestion.explanation && (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
                      <p className="text-blue-800 text-sm">
                        <strong>Explanation:</strong> {currentQuestion.explanation}
                      </p>
                    </div>
                  )}
                </div>

                {/* Answer Options */}
                <div className="space-y-3">
                  {currentQuestion.type === 'yes_no' && (
                    <div className="space-y-2">
                      {currentQuestion.options.map((option) => (
                        <label key={option.value} className="flex items-start cursor-pointer">
                          <input
                            type="radio"
                            name={currentQuestion.id}
                            value={option.value}
                            checked={responses[currentQuestion.id] === option.value}
                            onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                            className="mt-1 mr-3 text-primary-600 focus:ring-primary-500"
                          />
                          <div>
                            <div className="font-medium text-gray-900">{option.label}</div>
                            {option.description && (
                              <div className="text-sm text-gray-600 mt-1">{option.description}</div>
                            )}
                          </div>
                        </label>
                      ))}
                    </div>
                  )}

                  {currentQuestion.type === 'multiple_choice' && (
                    <div className="space-y-2">
                      {currentQuestion.options.map((option) => (
                        <label key={option.value} className="flex items-start cursor-pointer">
                          <input
                            type="radio"
                            name={currentQuestion.id}
                            value={option.value}
                            checked={responses[currentQuestion.id] === option.value}
                            onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                            className="mt-1 mr-3 text-primary-600 focus:ring-primary-500"
                          />
                          <div>
                            <div className="font-medium text-gray-900">{option.label}</div>
                            {option.description && (
                              <div className="text-sm text-gray-600 mt-1">{option.description}</div>
                            )}
                          </div>
                        </label>
                      ))}
                    </div>
                  )}

                  {currentQuestion.type === 'multiple_select' && (
                    <div className="space-y-2">
                      {currentQuestion.options.map((option) => (
                        <label key={option.value} className="flex items-start cursor-pointer">
                          <input
                            type="checkbox"
                            value={option.value}
                            checked={
                              Array.isArray(responses[currentQuestion.id]) &&
                              (responses[currentQuestion.id] as string[]).includes(option.value)
                            }
                            onChange={(e) => {
                              const currentValues = Array.isArray(responses[currentQuestion.id])
                                ? (responses[currentQuestion.id] as string[])
                                : [];

                              if (e.target.checked) {
                                handleAnswerChange(currentQuestion.id, [
                                  ...currentValues,
                                  option.value,
                                ]);
                              } else {
                                handleAnswerChange(
                                  currentQuestion.id,
                                  currentValues.filter((v: string) => v !== option.value)
                                );
                              }
                            }}
                            className="mt-1 mr-3 text-primary-600 focus:ring-primary-500 rounded"
                          />
                          <div>
                            <div className="font-medium text-gray-900">{option.label}</div>
                            {option.description && (
                              <div className="text-sm text-gray-600 mt-1">{option.description}</div>
                            )}
                          </div>
                        </label>
                      ))}
                    </div>
                  )}
                </div>

                {!showConsultationQuestion && (
                  <div className="mt-6 pt-4 border-t border-gray-200">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Additional Comments (Optional)
                      <span className="text-xs text-gray-500 ml-2">
                        {comments[currentQuestion.id]
                          ?.trim()
                          .split(/\s+/)
                          .filter((word) => word.length > 0).length || 0}
                        /150 words
                      </span>
                    </label>
                    <textarea
                      value={comments[currentQuestion.id] || ''}
                      onChange={(e) => handleCommentChange(currentQuestion.id, e.target.value)}
                      placeholder="Add any additional context, clarifications, or notes about your answer..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      rows={3}
                    />
                    {comments[currentQuestion.id]
                      ?.trim()
                      .split(/\s+/)
                      .filter((word) => word.length > 0).length > 150 && (
                      <p className="text-red-600 text-xs mt-1">Comment exceeds 150 word limit</p>
                    )}
                  </div>
                )}
              </div>

              {showConsultationQuestion && (
                <div className="card mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Consultation Interest
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Would you like to be contacted by EchoStor&apos;s Security Specialist for
                    consultation on any security matters?
                  </p>

                  <div className="space-y-3 mb-4">
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="consultation"
                        value="yes"
                        checked={consultationInterest === true}
                        onChange={() => setConsultationInterest(true)}
                        className="mr-3 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="font-medium text-gray-900">
                        Yes, I&apos;m interested in consultation
                      </span>
                    </label>
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="consultation"
                        value="no"
                        checked={consultationInterest === false}
                        onChange={() => setConsultationInterest(false)}
                        className="mr-3 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="font-medium text-gray-900">No, thank you</span>
                    </label>
                  </div>

                  {consultationInterest === true && (
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Consultation Details
                        <span className="text-xs text-gray-500 ml-2">
                          {
                            consultationDetails
                              .trim()
                              .split(/\s+/)
                              .filter((word) => word.length > 0).length
                          }
                          /300 words (10-300 words, optional)
                        </span>
                      </label>
                      <textarea
                        value={consultationDetails}
                        onChange={(e) => setConsultationDetails(e.target.value)}
                        placeholder="Please describe the security topics or areas you'd like to discuss with our specialist..."
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                        rows={5}
                      />
                      {(() => {
                        const wordCount = consultationDetails
                          .trim()
                          .split(/\s+/)
                          .filter((word) => word.length > 0).length;
                        if (wordCount > 0 && wordCount < 10) {
                          return (
                            <p className="text-orange-600 text-xs mt-1">
                              Please provide at least 10 words
                            </p>
                          );
                        } else if (wordCount > 300) {
                          return (
                            <p className="text-red-600 text-xs mt-1">Please limit to 300 words</p>
                          );
                        }
                        return null;
                      })()}
                    </div>
                  )}
                </div>
              )}

              {/* Navigation */}
              <div className="flex justify-between items-center">
                <button
                  onClick={goToPreviousQuestion}
                  disabled={
                    currentSectionIndex === 0 &&
                    currentQuestionIndex === 0 &&
                    !showConsultationQuestion
                  }
                  className="btn-secondary flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                  data-testid="previous-question-btn"
                >
                  <ChevronLeftIcon className="h-4 w-4 mr-2" />
                  Previous
                </button>

                <div className="flex space-x-4">
                  <button
                    onClick={saveProgress}
                    disabled={saveProgressMutation.isPending}
                    className="btn-secondary flex items-center"
                    data-testid="save-progress-btn"
                  >
                    <BookmarkIcon className="h-4 w-4 mr-2" />
                    {saveProgressMutation.isPending ? 'Saving...' : 'Save Progress'}
                  </button>

                  {isLastQuestion() ? (
                    <button
                      onClick={handleCompleteAssessment}
                      disabled={
                        completeAssessmentMutation.isPending ||
                        consultationInterest === null ||
                        (consultationInterest === true &&
                          consultationDetails.trim().length > 0 &&
                          (consultationDetails
                            .trim()
                            .split(/\s+/)
                            .filter((word) => word.length > 0).length < 10 ||
                            consultationDetails
                              .trim()
                              .split(/\s+/)
                              .filter((word) => word.length > 0).length > 300))
                      }
                      className="btn-primary flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                      data-testid="complete-assessment-btn"
                    >
                      <CheckCircleIcon className="h-4 w-4 mr-2" />
                      {completeAssessmentMutation.isPending
                        ? 'Completing...'
                        : 'Complete Assessment'}
                    </button>
                  ) : (
                    <button
                      onClick={goToNextQuestion}
                      disabled={!isCurrentQuestionAnswered()}
                      className="btn-primary flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                      data-testid="next-question-btn"
                    >
                      Next
                      <ChevronRightIcon className="h-4 w-4 ml-2" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </ErrorBoundary>
      </Layout>
    </ProtectedRoute>
  );
}
