import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import {
  ShieldCheckIcon,
  ChartBarIcon,
  DocumentTextIcon,
  UserGroupIcon,
  ArrowRightIcon,
} from '@heroicons/react/24/outline';

export default function Home() {
  const { user, isAdmin, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (isAdmin) {
        router.push('/admin');
      } else if (user) {
        router.push('/dashboard');
      }
    }
  }, [user, isAdmin, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <ShieldCheckIcon className="h-8 w-8 text-primary-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">
                Security Posture Assessment
              </h1>
            </div>
            <div className="flex space-x-4">
              <Link href="/auth/login" className="btn-secondary">
                Login
              </Link>
              <Link href="/auth/register" className="btn-primary">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
            Assess Your
            <span className="text-primary-600"> Security Posture</span>
          </h2>
          <p className="mt-6 max-w-2xl mx-auto text-xl text-gray-500">
            Comprehensive cybersecurity assessment across 19 key domains with 409 detailed
            questions. Get actionable insights and AI-powered recommendations to strengthen your
            security posture.
          </p>
          <div className="mt-10">
            <Link href="/auth/register" className="btn-primary text-lg px-8 py-3">
              Start Assessment
              <ArrowRightIcon className="ml-2 h-5 w-5 inline" />
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="mt-20">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <div className="card text-center">
              <DocumentTextIcon className="h-12 w-12 text-primary-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Comprehensive Assessment</h3>
              <p className="text-gray-600">
                409 questions across 19 security domains covering all aspects of cybersecurity
                maturity.
              </p>
            </div>

            <div className="card text-center">
              <ChartBarIcon className="h-12 w-12 text-primary-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Detailed Reports</h3>
              <p className="text-gray-600">
                Professional PDF reports with scoring, recommendations, and industry benchmarking.
              </p>
            </div>

            <div className="card text-center">
              <UserGroupIcon className="h-12 w-12 text-primary-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">AI-Enhanced Insights</h3>
              <p className="text-gray-600">
                ChatGPT-powered analysis providing intelligent recommendations and risk assessments.
              </p>
            </div>
          </div>
        </div>

        {/* How it works */}
        <div className="mt-20">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">How It Works</h3>
          <div className="grid grid-cols-1 gap-8 lg:grid-cols-4">
            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-600">1</span>
              </div>
              <h4 className="text-lg font-semibold mb-2">Sign Up</h4>
              <p className="text-gray-600">Create your account with company details</p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-600">2</span>
              </div>
              <h4 className="text-lg font-semibold mb-2">Complete Assessment</h4>
              <p className="text-gray-600">Answer questions across 19 security domains</p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-600">3</span>
              </div>
              <h4 className="text-lg font-semibold mb-2">Get Report</h4>
              <p className="text-gray-600">Receive detailed PDF report with scores</p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-600">4</span>
              </div>
              <h4 className="text-lg font-semibold mb-2">AI Insights</h4>
              <p className="text-gray-600">Request AI-enhanced analysis and recommendations</p>
            </div>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mt-20 bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h4 className="text-lg font-semibold text-yellow-800 mb-2">Important Disclaimer</h4>
          <p className="text-yellow-700">
            The outcomes delivered are best efforts based on general market practices and should not
            be considered as baseline for building security architecture. For detailed
            understanding, please contact our team for a more detailed and official
            security assessment.
          </p>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2024 Security Posture Assessment. All rights reserved.</p>
          <p className="mt-2 text-gray-400">
            Contact:{' '}
            <a href="mailto:contact@example.com" className="text-primary-400">
              contact@example.com
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}
