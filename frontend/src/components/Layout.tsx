import { ReactNode } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import {
  HomeIcon,
  DocumentTextIcon,
  ChartBarIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
  ChatBubbleLeftRightIcon,
  KeyIcon,
} from '@heroicons/react/24/outline';

interface LayoutProps {
  children: ReactNode;
  title?: string;
}

export default function Layout({ children, title }: LayoutProps) {
  const { user, isAdmin, logout } = useAuth();

  const navigation = isAdmin
    ? [
        { name: 'Dashboard', href: '/admin', icon: HomeIcon },
        { name: 'Users', href: '/admin/users', icon: UserIcon },
        { name: 'Assessments', href: '/admin/assessments', icon: DocumentTextIcon },
        { name: 'Reports', href: '/admin/reports', icon: ChartBarIcon },
        { name: 'Consultations', href: '/admin/consultations', icon: ChatBubbleLeftRightIcon },
        { name: 'OpenAI Keys', href: '/admin/openai-keys', icon: KeyIcon },
      ]
    : [
        { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
        { name: 'Assessment', href: '/assessment/start', icon: DocumentTextIcon },
        { name: 'Reports', href: '/reports', icon: ChartBarIcon },
      ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <Link href={isAdmin ? '/admin' : '/dashboard'}>
                  <span className="text-xl font-bold text-primary-600">
                    Security Assessment
                  </span>
                </Link>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  >
                    <item.icon className="w-4 h-4 mr-2" />
                    {item.name}
                  </Link>
                ))}
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {isAdmin ? (
                <span className="text-sm text-gray-700">Admin Panel</span>
              ) : user ? (
                <span className="text-sm text-gray-700">{user.full_name}</span>
              ) : null}
              <button
                onClick={logout}
                className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-500 hover:text-gray-700"
              >
                <ArrowRightOnRectangleIcon className="w-4 h-4 mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {title && (
          <div className="px-4 py-6 sm:px-0">
            <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
          </div>
        )}
        <div className="px-4 py-6 sm:px-0">{children}</div>
      </main>
    </div>
  );
}
