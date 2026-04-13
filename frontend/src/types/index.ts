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
