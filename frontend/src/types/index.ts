export interface SystemHealth {
  status: 'ok' | 'degraded';
  state_root: string;
  container_configured: boolean;
  container_health?: {
    ssh_ok: boolean;
    claude_ok: boolean;
    anthropic_api_key_ok: boolean;
    project_dir_writable: boolean;
    claude_version: string | null;
    gpu_models: string[];
    cuda_version: string | null;
    disk_free_bytes: number | null;
    warnings: string[];
  } | null;
  detail?: string | null;
}

export type TerminalSessionStatus = 'idle' | 'starting' | 'running' | 'stopping' | 'failed';

export interface TerminalSession {
  session_id: string | null;
  provider: 'ttyd';
  target_kind: 'daemon-host';
  status: TerminalSessionStatus;
  created_at: string | null;
  started_at: string | null;
  closed_at: string | null;
  terminal_url: string | null;
  detail: string | null;
}

export type CodeServerLifecycleStatus = 'starting' | 'ready' | 'unavailable';

export interface CodeServerStatus {
  status: CodeServerLifecycleStatus;
  workspace_dir: string | null;
  detail: string | null;
  managed: boolean;
}
