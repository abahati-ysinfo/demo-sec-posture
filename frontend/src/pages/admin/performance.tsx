import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import ErrorBoundary from '@/components/ErrorBoundary';
import {
  ClockIcon,
  CircleStackIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline';

export default function PerformanceDashboard() {
  const performanceBudgets = {
    apiResponseTime: { threshold: 500, unit: 'ms', status: 'good' },
    databaseQueryTime: { threshold: 100, unit: 'ms', status: 'good' },
    lcpScore: { threshold: 2500, unit: 'ms', status: 'good' },
    fidScore: { threshold: 100, unit: 'ms', status: 'good' },
    clsScore: { threshold: 0.1, unit: '', status: 'good' },
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'good':
        return 'text-green-600 bg-green-50';
      case 'warning':
        return 'text-yellow-600 bg-yellow-50';
      case 'poor':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'good':
        return 'Good';
      case 'warning':
        return 'Needs Improvement';
      case 'poor':
        return 'Poor';
      default:
        return 'Unknown';
    }
  };

  return (
    <ProtectedRoute adminOnly>
      <Layout title="Performance Monitoring">
        <ErrorBoundary>
          <div className="max-w-7xl mx-auto">
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Performance Monitoring</h2>
              <p className="text-gray-600">
                Monitor API response times, database queries, and user experience metrics
              </p>
            </div>

            {!process.env.NEXT_PUBLIC_SENTRY_DSN && (
              <div className="mb-6 card border-l-4 border-yellow-500 bg-yellow-50">
                <div className="flex items-start">
                  <ExclamationTriangleIcon className="h-6 w-6 text-yellow-600 mt-0.5 mr-3" />
                  <div>
                    <h3 className="text-sm font-semibold text-yellow-800 mb-1">
                      Sentry Not Configured
                    </h3>
                    <p className="text-sm text-yellow-700">
                      To enable full performance monitoring, set the following environment
                      variables:
                    </p>
                    <ul className="mt-2 text-sm text-yellow-700 list-disc list-inside space-y-1">
                      <li>
                        <code className="bg-yellow-100 px-1 py-0.5 rounded">
                          NEXT_PUBLIC_SENTRY_DSN
                        </code>{' '}
                        (frontend)
                      </li>
                      <li>
                        <code className="bg-yellow-100 px-1 py-0.5 rounded">SENTRY_DSN</code>{' '}
                        (backend)
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            )}

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Budgets</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="card">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center">
                      <ClockIcon className="h-6 w-6 text-blue-600 mr-2" />
                      <h4 className="font-semibold text-gray-900">API Response Time</h4>
                    </div>
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded ${getStatusColor(
                        performanceBudgets.apiResponseTime.status
                      )}`}
                    >
                      {getStatusText(performanceBudgets.apiResponseTime.status)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    Target: &lt; {performanceBudgets.apiResponseTime.threshold}
                    {performanceBudgets.apiResponseTime.unit}
                  </p>
                  <p className="text-xs text-gray-500">
                    Tracked via X-Response-Time header on all API endpoints
                  </p>
                </div>

                <div className="card">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center">
                      <CircleStackIcon className="h-6 w-6 text-purple-600 mr-2" />
                      <h4 className="font-semibold text-gray-900">Database Queries</h4>
                    </div>
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded ${getStatusColor(
                        performanceBudgets.databaseQueryTime.status
                      )}`}
                    >
                      {getStatusText(performanceBudgets.databaseQueryTime.status)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    Target: &lt; {performanceBudgets.databaseQueryTime.threshold}
                    {performanceBudgets.databaseQueryTime.unit}
                  </p>
                  <p className="text-xs text-gray-500">
                    Slow queries automatically logged and sent to Sentry
                  </p>
                </div>

                <div className="card">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center">
                      <ChartBarIcon className="h-6 w-6 text-green-600 mr-2" />
                      <h4 className="font-semibold text-gray-900">LCP (Loading)</h4>
                    </div>
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded ${getStatusColor(
                        performanceBudgets.lcpScore.status
                      )}`}
                    >
                      {getStatusText(performanceBudgets.lcpScore.status)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    Target: &lt; {performanceBudgets.lcpScore.threshold}
                    {performanceBudgets.lcpScore.unit}
                  </p>
                  <p className="text-xs text-gray-500">
                    Largest Contentful Paint - measures loading performance
                  </p>
                </div>

                <div className="card">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center">
                      <ChartBarIcon className="h-6 w-6 text-indigo-600 mr-2" />
                      <h4 className="font-semibold text-gray-900">FID (Interactivity)</h4>
                    </div>
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded ${getStatusColor(
                        performanceBudgets.fidScore.status
                      )}`}
                    >
                      {getStatusText(performanceBudgets.fidScore.status)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    Target: &lt; {performanceBudgets.fidScore.threshold}
                    {performanceBudgets.fidScore.unit}
                  </p>
                  <p className="text-xs text-gray-500">
                    First Input Delay - measures interactivity
                  </p>
                </div>

                <div className="card">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center">
                      <ChartBarIcon className="h-6 w-6 text-pink-600 mr-2" />
                      <h4 className="font-semibold text-gray-900">CLS (Stability)</h4>
                    </div>
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded ${getStatusColor(
                        performanceBudgets.clsScore.status
                      )}`}
                    >
                      {getStatusText(performanceBudgets.clsScore.status)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    Target: &lt; {performanceBudgets.clsScore.threshold}
                  </p>
                  <p className="text-xs text-gray-500">
                    Cumulative Layout Shift - measures visual stability
                  </p>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Monitoring & Observability
              </h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Backend Monitoring</h4>
                  <ul className="text-sm text-gray-600 space-y-2 list-disc list-inside">
                    <li>
                      <strong>API Performance:</strong> Response times tracked via middleware, added
                      to X-Response-Time header
                    </li>
                    <li>
                      <strong>Database Queries:</strong> SQLAlchemy event listeners track query
                      execution time
                    </li>
                    <li>
                      <strong>Slow Request Alerts:</strong> Requests &gt;500ms logged, &gt;1s sent
                      to Sentry
                    </li>
                    <li>
                      <strong>Slow Query Alerts:</strong> Queries &gt;100ms logged and sent to
                      Sentry
                    </li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Frontend Monitoring</h4>
                  <ul className="text-sm text-gray-600 space-y-2 list-disc list-inside">
                    <li>
                      <strong>Web Vitals:</strong> Core Web Vitals (LCP, FID, CLS) tracked
                      automatically
                    </li>
                    <li>
                      <strong>Additional Metrics:</strong> FCP and TTFB also tracked
                    </li>
                    <li>
                      <strong>Sentry Integration:</strong> Performance data sent to Sentry for
                      analysis
                    </li>
                    <li>
                      <strong>Console Logging:</strong> Metrics logged to console in development
                      mode
                    </li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">View Detailed Metrics</h4>
                  <p className="text-sm text-gray-600 mb-2">
                    For detailed performance metrics, transaction traces, and historical data:
                  </p>
                  <a
                    href="https://sentry.io"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center px-4 py-2 bg-purple-600 text-white text-sm font-medium rounded-md hover:bg-purple-700 transition-colors"
                  >
                    View in Sentry Dashboard →
                  </a>
                </div>
              </div>
            </div>
          </div>
        </ErrorBoundary>
      </Layout>
    </ProtectedRoute>
  );
}
