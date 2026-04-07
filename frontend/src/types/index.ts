// Type exports
export * from './task';
export * from './artifact';
export * from './context';

// Health check types
export interface SystemHealth {
  api_status: 'ok' | 'error' | 'degraded';
  ssh_available: boolean;
  workspace_ready: boolean;
  message?: string;
}