import { useEffect, useRef } from 'react';
import { useAuth } from './auth';
import { useRouter } from 'next/router';
import toast from 'react-hot-toast';

const INACTIVITY_TIMEOUT = 10 * 60 * 1000; // 10 minutes
const WARNING_TIMEOUT = 9 * 60 * 1000; // 9 minutes (1 minute warning)

export const useAutoLogout = (onBeforeLogout?: () => Promise<void>) => {
  const { logout } = useAuth();
  const router = useRouter();
  const timeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);
  const warningTimeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);

  const resetTimer = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);

    warningTimeoutRef.current = setTimeout(() => {
      toast('You will be logged out in 1 minute due to inactivity', {
        duration: 60000,
        icon: '⚠️',
      });
    }, WARNING_TIMEOUT);

    timeoutRef.current = setTimeout(async () => {
      if (onBeforeLogout) {
        try {
          await onBeforeLogout();
        } catch (error) {
          console.error('Error saving before logout:', error);
        }
      }
      logout();
      toast.error('Logged out due to inactivity');
      router.push('/auth/login');
    }, INACTIVITY_TIMEOUT);
  };

  useEffect(() => {
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];

    events.forEach((event) => {
      document.addEventListener(event, resetTimer, true);
    });

    resetTimer(); // Start the timer

    return () => {
      events.forEach((event) => {
        document.removeEventListener(event, resetTimer, true);
      });
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);
    };
  }, []);

  return { resetTimer };
};
