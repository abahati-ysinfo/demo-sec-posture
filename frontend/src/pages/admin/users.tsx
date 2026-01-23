import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Layout from '../../components/Layout';
import ProtectedRoute from '../../components/ProtectedRoute';
import ErrorBoundary from '../../components/ErrorBoundary';
import { adminAPI } from '../../lib/api';
import {
  UserIcon,
  MagnifyingGlassIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  TrashIcon,
  KeyIcon,
  ChevronUpIcon,
  ChevronDownIcon,
} from '@heroicons/react/24/outline';
import { toast } from 'react-hot-toast';

export default function AdminUsers() {
  const [search, setSearch] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState<{
    id: string;
    email: string;
    full_name: string;
    company_name: string;
    is_active: boolean;
    is_admin: boolean;
    is_protected: boolean;
    created_at: string;
  } | null>(null);
  const [selectedUsers, setSelectedUsers] = useState<string[]>([]);
  const [showBulkModal, setShowBulkModal] = useState(false);
  const [bulkOperation, setBulkOperation] = useState<'activate' | 'deactivate' | 'delete' | null>(
    null
  );
  const [newPassword, setNewPassword] = useState('');
  const limit = pageSize;
  const skip = (currentPage - 1) * limit;
  const queryClient = useQueryClient();

  const {
    data: usersData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['adminUsers', { skip, limit, search, sort_by: sortBy, sort_order: sortOrder }],
    queryFn: () =>
      adminAPI.getUsers({
        skip,
        limit,
        search: search || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
      }),
    placeholderData: (previousData) => previousData,
    refetchInterval: 30000,
  });

  const users = usersData?.data?.items || [];
  const pagination = usersData?.data;
  const hasNextPage = pagination?.has_next || false;
  const hasPrevPage = pagination?.has_prev || false;

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
  };

  const handleSort = (column: string) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
    setCurrentPage(1);
  };

  const handlePageSizeChange = (newSize: number) => {
    setPageSize(newSize);
    setCurrentPage(1);
  };

  const getSortIcon = (column: string) => {
    if (sortBy !== column) {
      return null;
    }
    return sortOrder === 'asc' ? (
      <ChevronUpIcon className="h-4 w-4 inline ml-1" />
    ) : (
      <ChevronDownIcon className="h-4 w-4 inline ml-1" />
    );
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const deleteUserMutation = useMutation({
    mutationFn: (userId: string) => adminAPI.deleteUser(userId),
    onSuccess: () => {
      toast.success('User deleted successfully');
      queryClient.invalidateQueries({ queryKey: ['adminUsers'] });
      setShowDeleteModal(false);
      setSelectedUser(null);
    },
    onError: () => {
      toast.error('Failed to delete user');
    },
  });

  const resetPasswordMutation = useMutation({
    mutationFn: ({ userId, password }: { userId: string; password: string }) =>
      adminAPI.resetUserPassword(userId, password),
    onSuccess: () => {
      toast.success('Password reset successfully');
      setShowPasswordModal(false);
      setSelectedUser(null);
      setNewPassword('');
    },
    onError: () => {
      toast.error('Failed to reset password');
    },
  });

  const bulkUpdateStatusMutation = useMutation({
    mutationFn: ({ userIds, isActive }: { userIds: string[]; isActive: boolean }) =>
      adminAPI.bulkUpdateUserStatus(userIds, isActive),
    onSuccess: (data) => {
      toast.success(`${data.data.message}`);
      queryClient.invalidateQueries({ queryKey: ['adminUsers'] });
      setSelectedUsers([]);
      setShowBulkModal(false);
      setBulkOperation(null);
    },
    onError: () => {
      toast.error('Failed to update users');
    },
  });

  const bulkDeleteMutation = useMutation({
    mutationFn: (userIds: string[]) => adminAPI.bulkDeleteUsers(userIds),
    onSuccess: (data) => {
      toast.success(`${data.data.message}`);
      queryClient.invalidateQueries({ queryKey: ['adminUsers'] });
      setSelectedUsers([]);
      setShowBulkModal(false);
      setBulkOperation(null);
    },
    onError: () => {
      toast.error('Failed to delete users');
    },
  });

  const handleDeleteUser = (user: {
    id: string;
    email: string;
    full_name: string;
    company_name: string;
    is_active: boolean;
    is_admin: boolean;
    is_protected: boolean;
    created_at: string;
  }) => {
    setSelectedUser(user);
    setShowDeleteModal(true);
  };

  const handleResetPassword = (user: {
    id: string;
    email: string;
    full_name: string;
    company_name: string;
    is_active: boolean;
    is_admin: boolean;
    is_protected: boolean;
    created_at: string;
  }) => {
    setSelectedUser(user);
    setShowPasswordModal(true);
  };

  const confirmDelete = () => {
    if (selectedUser) {
      deleteUserMutation.mutate(selectedUser.id);
    }
  };

  const confirmPasswordReset = () => {
    if (selectedUser && newPassword) {
      resetPasswordMutation.mutate({ userId: selectedUser.id, password: newPassword });
    }
  };

  const handleSelectAll = () => {
    const selectableUsers = users.filter(
      (user: {
        id: string;
        email: string;
        full_name: string;
        company_name: string;
        is_active: boolean;
        is_admin: boolean;
        is_protected: boolean;
        created_at: string;
      }) => !user.is_protected
    );

    if (selectedUsers.length === selectableUsers.length && selectableUsers.length > 0) {
      setSelectedUsers([]);
    } else {
      setSelectedUsers(selectableUsers.map((user) => user.id));
    }
  };

  const handleSelectUser = (userId: string) => {
    setSelectedUsers((prev) =>
      prev.includes(userId) ? prev.filter((id) => id !== userId) : [...prev, userId]
    );
  };

  const handleBulkOperation = (operation: 'activate' | 'deactivate' | 'delete') => {
    if (selectedUsers.length === 0) {
      toast.error('Please select users first');
      return;
    }
    setBulkOperation(operation);
    setShowBulkModal(true);
  };

  const confirmBulkOperation = () => {
    if (!bulkOperation || selectedUsers.length === 0) return;

    if (bulkOperation === 'delete') {
      bulkDeleteMutation.mutate(selectedUsers);
    } else {
      const isActive = bulkOperation === 'activate';
      bulkUpdateStatusMutation.mutate({ userIds: selectedUsers, isActive });
    }
  };

  return (
    <ProtectedRoute adminOnly>
      <Layout title="Users Management">
        <ErrorBoundary>
          <div className="max-w-7xl mx-auto">
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Users Management</h2>
              <p className="text-gray-600">View and manage all registered users in the system</p>
            </div>

            <div className="card mb-6">
              <form onSubmit={handleSearch} className="flex gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <MagnifyingGlassIcon className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search by name, email, or company..."
                      value={search}
                      onChange={(e) => setSearch(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    />
                  </div>
                </div>
                <button
                  type="submit"
                  className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Search
                </button>
              </form>
            </div>

            <div className="card">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">All Users ({users.length})</h3>
                <div className="flex items-center gap-4">
                  {selectedUsers.length > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-gray-600">{selectedUsers.length} selected</span>
                      <select
                        onChange={(e) => {
                          if (e.target.value) {
                            handleBulkOperation(
                              e.target.value as 'activate' | 'deactivate' | 'delete'
                            );
                            e.target.value = '';
                          }
                        }}
                        className="text-sm border border-gray-300 rounded px-2 py-1"
                        defaultValue=""
                      >
                        <option value="">Bulk Actions</option>
                        <option value="activate">Activate Users</option>
                        <option value="deactivate">Deactivate Users</option>
                        <option value="delete">Delete Users</option>
                      </select>
                    </div>
                  )}
                  <div className="flex items-center gap-2">
                    <select
                      value={pageSize}
                      onChange={(e) => handlePageSizeChange(Number(e.target.value))}
                      className="text-sm border border-gray-300 rounded px-2 py-1"
                    >
                      <option value={10}>10 per page</option>
                      <option value={20}>20 per page</option>
                      <option value={50}>50 per page</option>
                      <option value={100}>100 per page</option>
                    </select>
                  </div>
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
              </div>

              {isLoading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                  <p className="text-gray-600 mt-2">Loading users...</p>
                </div>
              ) : error ? (
                <div className="text-center py-8">
                  <p className="text-red-600">Error loading users. Please try again.</p>
                </div>
              ) : users.length === 0 ? (
                <div className="text-center py-8">
                  <UserIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">
                    {search ? 'No users found matching your search.' : 'No users found.'}
                  </p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">
                          <input
                            type="checkbox"
                            checked={selectedUsers.length === users.length && users.length > 0}
                            onChange={handleSelectAll}
                            className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                          />
                        </th>
                        <th
                          className="text-left py-3 px-4 font-semibold text-gray-900 cursor-pointer hover:bg-gray-50"
                          onClick={() => handleSort('full_name')}
                        >
                          User{getSortIcon('full_name')}
                        </th>
                        <th
                          className="text-left py-3 px-4 font-semibold text-gray-900 cursor-pointer hover:bg-gray-50"
                          onClick={() => handleSort('company_name')}
                        >
                          Company{getSortIcon('company_name')}
                        </th>
                        <th
                          className="text-left py-3 px-4 font-semibold text-gray-900 cursor-pointer hover:bg-gray-50"
                          onClick={() => handleSort('is_active')}
                        >
                          Status{getSortIcon('is_active')}
                        </th>
                        <th
                          className="text-left py-3 px-4 font-semibold text-gray-900 cursor-pointer hover:bg-gray-50"
                          onClick={() => handleSort('created_at')}
                        >
                          Joined{getSortIcon('created_at')}
                        </th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-900">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {users.map(
                        (user: {
                          id: string;
                          email: string;
                          full_name: string;
                          company_name: string;
                          is_active: boolean;
                          is_admin: boolean;
                          is_protected: boolean;
                          created_at: string;
                        }) => (
                          <tr key={user.id} className="border-b border-gray-100 hover:bg-gray-50">
                            <td className="py-4 px-4">
                              <input
                                type="checkbox"
                                checked={selectedUsers.includes(user.id)}
                                onChange={() => handleSelectUser(user.id)}
                                disabled={user.is_protected}
                                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                                title={user.is_protected ? 'Protected account' : ''}
                              />
                            </td>
                            <td className="py-4 px-4">
                              <div>
                                <div className="font-medium text-gray-900">{user.full_name}</div>
                                <div className="text-sm text-gray-600">{user.email}</div>
                              </div>
                            </td>
                            <td className="py-4 px-4">
                              <span className="text-gray-900">{user.company_name}</span>
                            </td>
                            <td className="py-4 px-4">
                              <span
                                className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                  user.is_active
                                    ? 'bg-green-100 text-green-800'
                                    : 'bg-red-100 text-red-800'
                                }`}
                              >
                                {user.is_active ? 'Active' : 'Inactive'}
                              </span>
                            </td>
                            <td className="py-4 px-4">
                              <span className="text-gray-600">{formatDate(user.created_at)}</span>
                            </td>
                            <td className="py-4 px-4">
                              <div className="flex space-x-2">
                                <button
                                  onClick={() => handleResetPassword(user)}
                                  className="text-indigo-600 hover:text-indigo-900 flex items-center"
                                  title="Reset Password"
                                >
                                  <KeyIcon className="h-4 w-4" />
                                </button>
                                <button
                                  onClick={() => handleDeleteUser(user)}
                                  disabled={user.is_protected}
                                  className={`flex items-center ${
                                    user.is_protected
                                      ? 'text-gray-400 cursor-not-allowed'
                                      : 'text-red-600 hover:text-red-900'
                                  }`}
                                  title={user.is_protected ? 'Protected account' : 'Delete User'}
                                >
                                  <TrashIcon className="h-4 w-4" />
                                </button>
                              </div>
                            </td>
                          </tr>
                        )
                      )}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* Delete Confirmation Modal */}
            {showDeleteModal && (
              <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
                <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                  <div className="mt-3 text-center">
                    <h3 className="text-lg font-medium text-gray-900">Delete User</h3>
                    <div className="mt-2 px-7 py-3">
                      <p className="text-sm text-gray-500">
                        Are you sure you want to delete {selectedUser?.full_name}? This action
                        cannot be undone.
                      </p>
                    </div>
                    <div className="flex justify-center space-x-4 mt-4">
                      <button onClick={() => setShowDeleteModal(false)} className="btn-secondary">
                        Cancel
                      </button>
                      <button
                        onClick={confirmDelete}
                        disabled={deleteUserMutation.isPending}
                        className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md disabled:opacity-50"
                      >
                        {deleteUserMutation.isPending ? 'Deleting...' : 'Delete'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Password Reset Modal */}
            {showPasswordModal && (
              <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
                <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                  <div className="mt-3">
                    <h3 className="text-lg font-medium text-gray-900 text-center">
                      Reset Password
                    </h3>
                    <div className="mt-4">
                      <label className="block text-sm font-medium text-gray-700">
                        New Password for {selectedUser?.full_name}
                      </label>
                      <input
                        type="password"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                        placeholder="Enter new password"
                      />
                    </div>
                    <div className="flex justify-center space-x-4 mt-6">
                      <button
                        onClick={() => {
                          setShowPasswordModal(false);
                          setNewPassword('');
                        }}
                        className="btn-secondary"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={confirmPasswordReset}
                        disabled={resetPasswordMutation.isPending || !newPassword}
                        className="btn-primary disabled:opacity-50"
                      >
                        {resetPasswordMutation.isPending ? 'Resetting...' : 'Reset Password'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Bulk Operation Confirmation Modal */}
            {showBulkModal && bulkOperation && (
              <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
                <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                  <div className="mt-3 text-center">
                    <h3 className="text-lg font-medium text-gray-900">
                      {bulkOperation === 'delete'
                        ? 'Delete Users'
                        : bulkOperation === 'activate'
                          ? 'Activate Users'
                          : 'Deactivate Users'}
                    </h3>
                    <div className="mt-2 px-7 py-3">
                      <p className="text-sm text-gray-500">
                        Are you sure you want to {bulkOperation} {selectedUsers.length} selected
                        user
                        {selectedUsers.length > 1 ? 's' : ''}?
                        {bulkOperation === 'delete' && ' This action cannot be undone.'}
                      </p>
                    </div>
                    <div className="flex justify-center space-x-4 mt-4">
                      <button
                        onClick={() => {
                          setShowBulkModal(false);
                          setBulkOperation(null);
                        }}
                        className="btn-secondary"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={confirmBulkOperation}
                        disabled={
                          bulkUpdateStatusMutation.isPending || bulkDeleteMutation.isPending
                        }
                        className={`px-4 py-2 rounded-md disabled:opacity-50 ${
                          bulkOperation === 'delete'
                            ? 'bg-red-600 hover:bg-red-700 text-white'
                            : 'btn-primary'
                        }`}
                      >
                        {bulkUpdateStatusMutation.isPending || bulkDeleteMutation.isPending
                          ? 'Processing...'
                          : `${
                              bulkOperation === 'delete'
                                ? 'Delete'
                                : bulkOperation === 'activate'
                                  ? 'Activate'
                                  : 'Deactivate'
                            }`}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </ErrorBoundary>
      </Layout>
    </ProtectedRoute>
  );
}
