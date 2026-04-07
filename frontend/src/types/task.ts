// Task Read Model Contract Types
// Based on docs/LLM-Working/refactoring-plan/task-read-model-contract.md

import type { ArtifactPreview } from './artifact';

export type TaskMode = 'bounded-discovery' | 'bounded-reproduction';
export type TaskStatus = 'running' | 'completed' | 'failed' | 'cancelled' | 'blocked';

export interface TaskIdentity {
  task_id: string;
  mode: TaskMode;
  created_at: string;
  updated_at: string;
}

export interface TaskLifecycle {
  status: TaskStatus;
  stage: string;
  termination_reason: string | null;
  active_gate: string | null;
}

export interface TaskInputSummary {
  title: string;
  brief: string;
  seed_inputs: string[];
  target_inputs: string[];
}

export interface TaskProgressSummary {
  current_checkpoint: string;
  milestones: Milestone[];
  recent_events: EventSummary[];
  artifact_counts: ArtifactCounts;
}

export interface Milestone {
  id: string;
  name: string;
  status: 'completed' | 'in_progress' | 'failed' | 'blocked';
  timestamp: string;
}

export interface EventSummary {
  id: string;
  message: string;
  timestamp: string;
}

export interface ArtifactCounts {
  tables: number;
  reports: number;
  figures: number;
}

export interface TaskResultSummary {
  result_brief: string | null;
  termination_reason: string | null;
  recent_artifacts: ArtifactPreview[];
  error_summary: string | null;
}

// Full Task Read Model
export interface TaskReadModel {
  identity: TaskIdentity;
  lifecycle: TaskLifecycle;
  input_summary: TaskInputSummary;
  progress_summary: TaskProgressSummary;
  result_summary: TaskResultSummary;
}

// List Item (minimal fields for homepage)
export interface TaskListItem {
  task_id: string;
  mode: TaskMode;
  title: string;
  status: TaskStatus;
  stage: string;
  updated_at: string;
  termination_reason: string | null;
}