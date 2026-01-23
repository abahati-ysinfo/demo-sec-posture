/**
 * Cross-tab synchronization utility using BroadcastChannel API
 * Falls back to localStorage events for browsers that don't support BroadcastChannel
 */

export enum SyncEventType {
  ASSESSMENT_STARTED = 'ASSESSMENT_STARTED',
  PROGRESS_SAVED = 'PROGRESS_SAVED',
  ASSESSMENT_COMPLETED = 'ASSESSMENT_COMPLETED',
}

export interface SyncEvent {
  type: SyncEventType;
  assessmentId: string;
  timestamp: number;
  originTabId?: string;
  data?: unknown;
}

type SyncEventHandler = (event: SyncEvent) => void;

const CHANNEL_NAME = 'echostor-assessment-sync';
const STORAGE_KEY = 'echostor-sync-event';

class CrossTabSync {
  private channel: BroadcastChannel | null = null;
  private listeners: Set<SyncEventHandler> = new Set();
  private useLocalStorage = false;
  private tabId: string;

  constructor() {
    this.tabId = `tab-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    if (typeof window === 'undefined') return;

    if (typeof BroadcastChannel !== 'undefined') {
      this.channel = new BroadcastChannel(CHANNEL_NAME);
      this.channel.onmessage = (event: MessageEvent<SyncEvent>) => {
        this.notifyListeners(event.data);
      };
    } else {
      this.useLocalStorage = true;
      window.addEventListener('storage', this.handleStorageEvent);
    }
  }

  private handleStorageEvent = (event: StorageEvent) => {
    if (event.key === STORAGE_KEY && event.newValue) {
      try {
        const syncEvent: SyncEvent = JSON.parse(event.newValue);
        this.notifyListeners(syncEvent);
      } catch (error) {
        console.error('Failed to parse sync event from localStorage:', error);
      }
    }
  };

  private notifyListeners(event: SyncEvent) {
    this.listeners.forEach((listener) => {
      try {
        listener(event);
      } catch (error) {
        console.error('Error in sync event listener:', error);
      }
    });
  }

  public broadcast(type: SyncEventType, assessmentId: string, data?: unknown) {
    const event: SyncEvent = {
      type,
      assessmentId,
      timestamp: Date.now(),
      originTabId: this.tabId,
      data,
    };

    if (this.channel) {
      this.channel.postMessage(event);
    } else if (this.useLocalStorage) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(event));
      setTimeout(() => {
        localStorage.removeItem(STORAGE_KEY);
      }, 100);
    }
  }

  public getTabId(): string {
    return this.tabId;
  }

  public subscribe(handler: SyncEventHandler): () => void {
    this.listeners.add(handler);
    return () => {
      this.listeners.delete(handler);
    };
  }

  public destroy() {
    if (this.channel) {
      this.channel.close();
      this.channel = null;
    }
    if (this.useLocalStorage) {
      window.removeEventListener('storage', this.handleStorageEvent);
    }
    this.listeners.clear();
  }
}

export const crossTabSync = new CrossTabSync();
