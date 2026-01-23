import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Layout from '@/components/Layout';
import ProtectedRoute from '@/components/ProtectedRoute';
import ErrorBoundary from '@/components/ErrorBoundary';
import { adminAPI } from '@/lib/api';
import {
  KeyIcon,
  PlusIcon,
  TrashIcon,
  CheckCircleIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import type { OpenAIKey } from '@/lib/apiTypes';

export default function OpenAIKeysManagement() {
  const queryClient = useQueryClient();
  const [showAddModal, setShowAddModal] = useState(false);
  const [showTestModal, setShowTestModal] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [newApiKey, setNewApiKey] = useState('');
  const [testApiKey, setTestApiKey] = useState('');
  const [testResult, setTestResult] = useState<{ success: boolean; message: string } | null>(null);

  const { data: keys, isLoading } = useQuery({
    queryKey: ['openaiKeys'],
    queryFn: () => adminAPI.listOpenAIKeys(true),
    refetchInterval: 30000,
  });

  const addKeyMutation = useMutation({
    mutationFn: (data: { key_name: string; api_key: string }) => adminAPI.createOpenAIKey(data),
    onSuccess: () => {
      toast.success('API key added successfully');
      setShowAddModal(false);
      setNewKeyName('');
      setNewApiKey('');
      queryClient.invalidateQueries({ queryKey: ['openaiKeys'] });
    },
    onError: (error: unknown) => {
      toast.error(
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
          'Failed to add API key'
      );
    },
  });

  const toggleKeyMutation = useMutation({
    mutationFn: (data: { key_id: string; is_active: boolean }) =>
      adminAPI.toggleOpenAIKey(data.key_id, data.is_active),
    onSuccess: () => {
      toast.success('API key status updated');
      queryClient.invalidateQueries({ queryKey: ['openaiKeys'] });
    },
    onError: (error: unknown) => {
      toast.error(
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
          'Failed to update API key'
      );
    },
  });

  const deleteKeyMutation = useMutation({
    mutationFn: (key_id: string) => adminAPI.deleteOpenAIKey(key_id),
    onSuccess: () => {
      toast.success('API key deleted successfully');
      queryClient.invalidateQueries({ queryKey: ['openaiKeys'] });
    },
    onError: (error: unknown) => {
      toast.error(
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
          'Failed to delete API key'
      );
    },
  });

  const testKeyMutation = useMutation({
    mutationFn: (api_key: string) => adminAPI.testOpenAIKey(api_key),
    onSuccess: (data) => {
      setTestResult(data.data);
    },
    onError: (error: unknown) => {
      setTestResult({
        success: false,
        message:
          (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
          'Test failed',
      });
    },
  });

  const handleAddKey = () => {
    if (!newKeyName.trim() || !newApiKey.trim()) {
      toast.error('Please provide both key name and API key');
      return;
    }
    addKeyMutation.mutate({ key_name: newKeyName, api_key: newApiKey });
  };

  const handleTestKey = () => {
    if (!testApiKey.trim()) {
      toast.error('Please provide an API key to test');
      return;
    }
    setTestResult(null);
    testKeyMutation.mutate(testApiKey);
  };

  const handleDeleteKey = (keyId: string, keyName: string) => {
    if (confirm(`Are you sure you want to delete the API key "${keyName}"?`)) {
      deleteKeyMutation.mutate(keyId);
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Never';
    return new Date(dateString).toLocaleString();
  };

  const getStatusBadge = (key: OpenAIKey) => {
    if (!key.is_active) {
      return (
        <span className="px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">
          Inactive
        </span>
      );
    }
    if (key.cooldown_until && new Date(key.cooldown_until) > new Date()) {
      return (
        <span className="px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
          Cooldown
        </span>
      );
    }
    if (key.error_count >= 3) {
      return (
        <span className="px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800">
          Errors
        </span>
      );
    }
    return (
      <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
        Active
      </span>
    );
  };

  return (
    <ProtectedRoute adminOnly>
      <Layout title="OpenAI API Keys Management">
        <ErrorBoundary>
          <div className="max-w-7xl mx-auto">
            <div className="mb-8 flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">OpenAI API Keys</h2>
                <p className="text-gray-600">
                  Manage OpenAI API keys for AI-enhanced report generation with round-robin rotation
                </p>
              </div>
              <div className="flex gap-3">
                <button
                  onClick={() => setShowTestModal(true)}
                  className="btn-secondary flex items-center"
                >
                  <CheckCircleIcon className="h-5 w-5 mr-2" />
                  Test Key
                </button>
                <button
                  onClick={() => setShowAddModal(true)}
                  className="btn-primary flex items-center"
                >
                  <PlusIcon className="h-5 w-5 mr-2" />
                  Add API Key
                </button>
              </div>
            </div>

            {isLoading ? (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
                <p className="text-gray-600 mt-4">Loading API keys...</p>
              </div>
            ) : keys?.data?.length === 0 ? (
              <div className="card text-center py-12">
                <KeyIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No API Keys Configured</h3>
                <p className="text-gray-600 mb-6">
                  Add your first OpenAI API key to enable AI-enhanced report generation
                </p>
                <button
                  onClick={() => setShowAddModal(true)}
                  className="btn-primary inline-flex items-center"
                >
                  <PlusIcon className="h-5 w-5 mr-2" />
                  Add Your First API Key
                </button>
              </div>
            ) : (
              <div className="card overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Key Name
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          API Key
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Usage
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Last Used
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Errors
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {keys?.data?.map((key) => (
                        <tr key={key.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <KeyIcon className="h-5 w-5 text-gray-400 mr-2" />
                              <div>
                                <div className="text-sm font-medium text-gray-900">
                                  {key.key_name}
                                </div>
                                <div className="text-xs text-gray-500">
                                  Added {formatDate(key.created_at)}
                                </div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <code className="text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded">
                              {key.masked_key}
                            </code>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">{getStatusBadge(key)}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {key.usage_count} times
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {formatDate(key.last_used_at)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span
                              className={`text-sm font-medium ${
                                key.error_count >= 3
                                  ? 'text-red-600'
                                  : key.error_count > 0
                                    ? 'text-yellow-600'
                                    : 'text-green-600'
                              }`}
                            >
                              {key.error_count}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <div className="flex items-center gap-2">
                              <button
                                onClick={() =>
                                  toggleKeyMutation.mutate({
                                    key_id: key.id,
                                    is_active: !key.is_active,
                                  })
                                }
                                className={`${
                                  key.is_active
                                    ? 'text-yellow-600 hover:text-yellow-900'
                                    : 'text-green-600 hover:text-green-900'
                                }`}
                                title={key.is_active ? 'Deactivate' : 'Activate'}
                              >
                                {key.is_active ? (
                                  <XCircleIcon className="h-5 w-5" />
                                ) : (
                                  <CheckCircleIcon className="h-5 w-5" />
                                )}
                              </button>
                              <button
                                onClick={() => handleDeleteKey(key.id, key.key_name)}
                                className="text-red-600 hover:text-red-900"
                                title="Delete"
                              >
                                <TrashIcon className="h-5 w-5" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {keys?.data && keys.data.length > 0 && (
              <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="card">
                  <h4 className="text-sm font-medium text-gray-500 mb-2">Total Keys</h4>
                  <p className="text-2xl font-bold text-gray-900">{keys.data.length}</p>
                </div>
                <div className="card">
                  <h4 className="text-sm font-medium text-gray-500 mb-2">Active Keys</h4>
                  <p className="text-2xl font-bold text-green-600">
                    {keys.data.filter((k) => k.is_active).length}
                  </p>
                </div>
                <div className="card">
                  <h4 className="text-sm font-medium text-gray-500 mb-2">Total Usage</h4>
                  <p className="text-2xl font-bold text-blue-600">
                    {keys.data.reduce((sum, k) => sum + k.usage_count, 0)}
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Add Key Modal */}
          {showAddModal && (
            <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
              <div className="relative top-20 mx-auto p-5 border w-full max-w-md shadow-lg rounded-md bg-white">
                <div className="mt-3">
                  <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">
                    Add New OpenAI API Key
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Key Name
                      </label>
                      <input
                        type="text"
                        value={newKeyName}
                        onChange={(e) => setNewKeyName(e.target.value)}
                        placeholder="e.g., Production Key 1"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        API Key
                      </label>
                      <input
                        type="password"
                        value={newApiKey}
                        onChange={(e) => setNewApiKey(e.target.value)}
                        placeholder="sk-..."
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        The key will be encrypted and stored securely
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3 mt-6">
                    <button
                      onClick={handleAddKey}
                      disabled={addKeyMutation.isPending}
                      className="flex-1 btn-primary"
                    >
                      {addKeyMutation.isPending ? 'Adding...' : 'Add Key'}
                    </button>
                    <button
                      onClick={() => {
                        setShowAddModal(false);
                        setNewKeyName('');
                        setNewApiKey('');
                      }}
                      className="flex-1 btn-secondary"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Test Key Modal */}
          {showTestModal && (
            <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
              <div className="relative top-20 mx-auto p-5 border w-full max-w-md shadow-lg rounded-md bg-white">
                <div className="mt-3">
                  <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">
                    Test OpenAI API Key
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        API Key
                      </label>
                      <input
                        type="password"
                        value={testApiKey}
                        onChange={(e) => setTestApiKey(e.target.value)}
                        placeholder="sk-..."
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>
                    {testResult && (
                      <div
                        className={`p-3 rounded-md ${
                          testResult.success
                            ? 'bg-green-50 border border-green-200'
                            : 'bg-red-50 border border-red-200'
                        }`}
                      >
                        <div className="flex items-center">
                          {testResult.success ? (
                            <CheckCircleIcon className="h-5 w-5 text-green-600 mr-2" />
                          ) : (
                            <XCircleIcon className="h-5 w-5 text-red-600 mr-2" />
                          )}
                          <p
                            className={`text-sm ${
                              testResult.success ? 'text-green-800' : 'text-red-800'
                            }`}
                          >
                            {testResult.message}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                  <div className="flex gap-3 mt-6">
                    <button
                      onClick={handleTestKey}
                      disabled={testKeyMutation.isPending}
                      className="flex-1 btn-primary"
                    >
                      {testKeyMutation.isPending ? 'Testing...' : 'Test Key'}
                    </button>
                    <button
                      onClick={() => {
                        setShowTestModal(false);
                        setTestApiKey('');
                        setTestResult(null);
                      }}
                      className="flex-1 btn-secondary"
                    >
                      Close
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </ErrorBoundary>
      </Layout>
    </ProtectedRoute>
  );
}
