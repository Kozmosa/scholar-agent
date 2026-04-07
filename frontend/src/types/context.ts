// Workspace / Session / Container Summary Contract Types
// Based on docs/LLM-Working/refactoring-plan/workspace-session-container-summary-contract.md

export type SessionStatus = 'active' | 'inactive' | 'error';
export type EnvironmentStatus = 'ready' | 'not_ready' | 'error';

export interface WorkspaceSummary {
  workspace_id: string;
  workspace_label: string;
  project_dir: string;
}

export interface SessionSummary {
  session_status: SessionStatus;
  connected: boolean;
  recoverable: boolean;
}

export interface ContainerSummary {
  container_label: string;
  ssh_available: boolean;
  environment_status: EnvironmentStatus;
}

export interface ResourceSnapshot {
  gpu: number | null;  // percentage
  cpu: number;         // percentage
  memory: number;      // percentage
  disk: number;        // percentage
}

// Combined execution context
export interface ExecutionContextSummary {
  workspace: WorkspaceSummary;
  session: SessionSummary;
  container: ContainerSummary;
  resource_snapshot: ResourceSnapshot;
}