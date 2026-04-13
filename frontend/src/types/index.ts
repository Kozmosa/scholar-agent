export interface SystemHealth {
  api_status: 'ok' | 'error' | 'degraded';
  ssh_available: boolean;
  workspace_ready: boolean;
  message?: string;
}
