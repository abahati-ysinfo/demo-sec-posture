import React, { useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import ProtectedRoute from '../components/ProtectedRoute';

export default function Assessment() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/assessment/start');
  }, [router]);

  return (
    <ProtectedRoute>
      <Layout title="Assessment">
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
            <p className="text-gray-600 mt-2">Redirecting to assessment...</p>
          </div>
        </div>
      </Layout>
    </ProtectedRoute>
  );
}
