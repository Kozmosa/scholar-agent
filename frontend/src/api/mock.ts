import type { SystemHealth, TerminalSession } from '../types';

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

let mockTerminalSession: TerminalSession = {
  session_id: null,
  provider: 'ttyd',
  target_kind: 'daemon-host',
  status: 'idle',
  created_at: null,
  started_at: null,
  closed_at: null,
  terminal_url: null,
  detail: null,
};

export function mockGetHealth(): SystemHealth {
  return mockHealth;
}

export function mockGetTerminalSession(): TerminalSession {
  return mockTerminalSession;
}

export function mockCreateTerminalSession(): TerminalSession {
  const timestamp = new Date().toISOString();

  mockTerminalSession = {
    session_id: 'mock-terminal-session',
    provider: 'ttyd',
    target_kind: 'daemon-host',
    status: 'running',
    created_at: mockTerminalSession.created_at ?? timestamp,
    started_at: timestamp,
    closed_at: null,
    terminal_url: 'http://127.0.0.1:7681',
    detail: null,
  };

  return mockTerminalSession;
}

export function mockDeleteTerminalSession(): TerminalSession {
  mockTerminalSession = {
    session_id: null,
    provider: 'ttyd',
    target_kind: 'daemon-host',
    status: 'idle',
    created_at: mockTerminalSession.created_at,
    started_at: mockTerminalSession.started_at,
    closed_at: new Date().toISOString(),
    terminal_url: null,
    detail: null,
  };

  return mockTerminalSession;
}
