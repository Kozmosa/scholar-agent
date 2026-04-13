import type { SystemHealth } from '../types';

const mockHealth: SystemHealth = {
  api_status: 'ok',
  ssh_available: true,
  workspace_ready: true,
  message: 'Mock health response for frontend development mode.',
};

export function mockGetHealth(): SystemHealth {
  return mockHealth;
}
