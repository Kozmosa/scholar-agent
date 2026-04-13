import type { SystemHealth } from '../types';

const mockHealth: SystemHealth = {
  status: 'ok',
  state_root: '.ainrf',
  container_configured: true,
  container_health: {
    ssh_ok: true,
    claude_ok: true,
    anthropic_api_key_ok: true,
    project_dir_writable: true,
    claude_version: 'mock',
    gpu_models: ['Mock GPU'],
    cuda_version: 'mock',
    disk_free_bytes: 1024 * 1024 * 1024,
    warnings: [],
  },
  detail: null,
};

export function mockGetHealth(): SystemHealth {
  return mockHealth;
}
