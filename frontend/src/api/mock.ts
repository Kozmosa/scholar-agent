import type {
  AnthropicEnvStatus,
  CodeServerStatus,
  EnvironmentCreateRequest,
  EnvironmentListResponse,
  EnvironmentRecord,
  EnvironmentUpdateRequest,
  SystemHealth,
  TerminalSession,
} from '../types';

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

const mockCodeServerStatus: CodeServerStatus = {
  status: 'ready',
  workspace_dir: '/workspace/projects/demo',
  detail: null,
  managed: true,
};

let mockEnvironmentCounter = 0;
let mockEnvironments: EnvironmentRecord[] = [];

function nowIso(): string {
  return new Date().toISOString();
}

function cloneEnvironment(environment: EnvironmentRecord): EnvironmentRecord {
  return {
    ...environment,
    tags: [...environment.tags],
    ssh_options: { ...environment.ssh_options },
    latest_detection: environment.latest_detection
      ? {
          ...environment.latest_detection,
          errors: [...environment.latest_detection.errors],
          warnings: [...environment.latest_detection.warnings],
          gpu_models: [...environment.latest_detection.gpu_models],
          python: { ...environment.latest_detection.python },
          conda: { ...environment.latest_detection.conda },
          uv: { ...environment.latest_detection.uv },
          pixi: { ...environment.latest_detection.pixi },
          torch: { ...environment.latest_detection.torch },
          cuda: { ...environment.latest_detection.cuda },
          claude_cli: { ...environment.latest_detection.claude_cli },
        }
      : null,
  };
}

function createToolStatus(
  available: boolean,
  version: string | null = null,
  path: string | null = null
): { available: boolean; version: string | null; path: string | null } {
  return { available, version, path };
}

function createMockEnvironment(
  payload: EnvironmentCreateRequest | EnvironmentUpdateRequest,
  existing?: EnvironmentRecord
): EnvironmentRecord {
  const timestamp = nowIso();
  const id = existing?.id ?? `env-${++mockEnvironmentCounter}`;
  return {
    id,
    alias: payload.alias ?? existing?.alias ?? 'mock-env',
    display_name: payload.display_name ?? existing?.display_name ?? 'Mock Environment',
    description: payload.description ?? existing?.description ?? null,
    tags: payload.tags ?? existing?.tags ?? [],
    host: payload.host ?? existing?.host ?? 'mock.example.com',
    port: payload.port ?? existing?.port ?? 22,
    user: payload.user ?? existing?.user ?? 'root',
    auth_kind: payload.auth_kind ?? existing?.auth_kind ?? 'ssh_key',
    identity_file: payload.identity_file ?? existing?.identity_file ?? null,
    proxy_jump: payload.proxy_jump ?? existing?.proxy_jump ?? null,
    proxy_command: payload.proxy_command ?? existing?.proxy_command ?? null,
    ssh_options: payload.ssh_options ?? existing?.ssh_options ?? {},
    default_workdir: payload.default_workdir ?? existing?.default_workdir ?? null,
    preferred_python: payload.preferred_python ?? existing?.preferred_python ?? null,
    preferred_env_manager: payload.preferred_env_manager ?? existing?.preferred_env_manager ?? null,
    preferred_runtime_notes: payload.preferred_runtime_notes ?? existing?.preferred_runtime_notes ?? null,
    created_at: existing?.created_at ?? timestamp,
    updated_at: timestamp,
    latest_detection: existing?.latest_detection ?? null,
  };
}

function createMockDetection(environment: EnvironmentRecord): EnvironmentRecord['latest_detection'] {
  const timestamp = nowIso();
  return {
    environment_id: environment.id,
    detected_at: timestamp,
    status: 'success',
    summary: `Manual detection completed for ${environment.alias}.`,
    errors: [],
    warnings: [],
    ssh_ok: true,
    hostname: environment.host,
    os_info: 'linux',
    arch: 'x86_64',
    workdir_exists: Boolean(environment.default_workdir),
    python: createToolStatus(true, environment.preferred_python ?? 'python3', '/usr/bin/python3'),
    conda: createToolStatus(false),
    uv: createToolStatus(true, 'mock', '/usr/bin/uv'),
    pixi: createToolStatus(false),
    torch: createToolStatus(false),
    cuda: createToolStatus(false),
    gpu_models: [],
    gpu_count: 0,
    claude_cli: createToolStatus(true, 'mock', '/usr/bin/claude'),
    anthropic_env: 'unknown' as AnthropicEnvStatus,
  };
}

let mockTerminalSession: TerminalSession = {
  session_id: null,
  provider: 'pty',
  target_kind: 'daemon-host',
  status: 'idle',
  created_at: null,
  started_at: null,
  closed_at: null,
  terminal_ws_url: null,
  detail: null,
};

const initialTerminalSession: TerminalSession = mockTerminalSession;
const initialMockEnvironments: EnvironmentRecord[] = [...mockEnvironments];

export function mockGetHealth(): SystemHealth {
  return mockHealth;
}

export function mockGetCodeServerStatus(): CodeServerStatus {
  return mockCodeServerStatus;
}

export function mockGetTerminalSession(): TerminalSession {
  return mockTerminalSession;
}

export function mockCreateTerminalSession(): TerminalSession {
  const timestamp = new Date().toISOString();

  mockTerminalSession = {
    session_id: 'mock-terminal-session',
    provider: 'pty',
    target_kind: 'daemon-host',
    status: 'running',
    created_at: mockTerminalSession.created_at ?? timestamp,
    started_at: timestamp,
    closed_at: null,
    terminal_ws_url: 'ws://127.0.0.1:8000/terminal/session/mock-terminal-session/ws?token=mock-token',
    detail: null,
  };

  return mockTerminalSession;
}

export function mockDeleteTerminalSession(): TerminalSession {
  mockTerminalSession = {
    session_id: null,
    provider: 'pty',
    target_kind: 'daemon-host',
    status: 'idle',
    created_at: mockTerminalSession.created_at,
    started_at: mockTerminalSession.started_at,
    closed_at: new Date().toISOString(),
    terminal_ws_url: null,
    detail: null,
  };

  return mockTerminalSession;
}

export function resetMockTerminalSession(): TerminalSession {
  mockTerminalSession = { ...initialTerminalSession };
  return mockTerminalSession;
}

export function mockGetEnvironments(): EnvironmentListResponse {
  return {
    items: mockEnvironments.map((environment) => cloneEnvironment(environment)),
  };
}

export function mockGetEnvironment(environmentId: string): EnvironmentRecord {
  const environment = mockEnvironments.find((item) => item.id === environmentId);
  if (!environment) {
    throw new Error(`Environment not found: ${environmentId}`);
  }
  return cloneEnvironment(environment);
}

export function mockCreateEnvironment(payload: EnvironmentCreateRequest): EnvironmentRecord {
  const environment = createMockEnvironment(payload);
  mockEnvironments = [...mockEnvironments, environment];
  return cloneEnvironment(environment);
}

export function mockUpdateEnvironment(
  environmentId: string,
  payload: EnvironmentUpdateRequest
): EnvironmentRecord {
  const current = mockEnvironments.find((environment) => environment.id === environmentId);
  if (!current) {
    throw new Error(`Environment not found: ${environmentId}`);
  }
  const updated = createMockEnvironment(payload, current);
  mockEnvironments = mockEnvironments.map((environment) =>
    environment.id === environmentId ? updated : environment
  );
  return cloneEnvironment(updated);
}

export function mockDeleteEnvironment(environmentId: string): void {
  mockEnvironments = mockEnvironments.filter((environment) => environment.id !== environmentId);
}

export function mockDetectEnvironment(environmentId: string): EnvironmentRecord {
  const current = mockEnvironments.find((environment) => environment.id === environmentId);
  if (!current) {
    throw new Error(`Environment not found: ${environmentId}`);
  }
  const updated = {
    ...current,
    latest_detection: createMockDetection(current),
    updated_at: nowIso(),
  };
  mockEnvironments = mockEnvironments.map((environment) =>
    environment.id === environmentId ? updated : environment
  );
  return cloneEnvironment(updated);
}

export function resetMockEnvironmentState(): EnvironmentListResponse {
  mockEnvironmentCounter = 0;
  mockEnvironments = [...initialMockEnvironments];
  return mockGetEnvironments();
}
