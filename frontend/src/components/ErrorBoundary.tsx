import React from 'react';
import { ErrorBoundary as ReactErrorBoundary, FallbackProps } from 'react-error-boundary';

interface ErrorBoundaryProps {
  children: React.ReactNode;
}

function ErrorFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="card max-w-md w-full">
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
            <svg
              className="h-6 w-6 text-red-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Something went wrong</h3>
          <p className="text-gray-600 mb-4">
            We encountered an unexpected error. Please try again or contact support if the problem
            persists.
          </p>
          {error && (
            <details className="text-left mb-4">
              <summary className="text-sm text-gray-500 cursor-pointer hover:text-gray-700">
                Error details
              </summary>
              <pre className="mt-2 text-xs text-red-600 bg-red-50 p-3 rounded overflow-auto max-h-32">
                {error.message}
              </pre>
            </details>
          )}
          <div className="flex gap-3 justify-center">
            <button onClick={resetErrorBoundary} className="btn-primary">
              Try Again
            </button>
            <button
              onClick={() => {
                if (typeof window !== 'undefined') {
                  window.location.href = '/';
                }
              }}
              className="btn-secondary"
            >
              Go Home
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function logErrorToService(error: Error, errorInfo: React.ErrorInfo) {
  if (typeof window !== 'undefined' && (window as { Sentry?: unknown }).Sentry) {
    (
      window as unknown as { Sentry: { captureException: (err: Error, opts: unknown) => void } }
    ).Sentry.captureException(error, {
      contexts: {
        react: {
          componentStack: errorInfo.componentStack,
        },
      },
    });
  } else {
    console.error('Error caught by boundary:', error, errorInfo);
  }
}

export default function ErrorBoundary({ children }: ErrorBoundaryProps) {
  return (
    <ReactErrorBoundary FallbackComponent={ErrorFallback} onError={logErrorToService}>
      {children}
    </ReactErrorBoundary>
  );
}
