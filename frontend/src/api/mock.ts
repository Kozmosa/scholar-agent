// Mock API responses for development
// In production, these would be served by the actual backend

import type {
  TaskListItem,
  TaskReadModel,
  ArtifactListItem,
  ArtifactPreview,
  ExecutionContextSummary,
  SystemHealth,
} from '../types';

// Mock data generators
const mockTasks: TaskListItem[] = [
  {
    task_id: 'task-001',
    mode: 'bounded-discovery',
    title: 'Attention Mechanism Survey',
    status: 'running',
    stage: 'literature-search',
    updated_at: new Date().toISOString(),
    termination_reason: null,
  },
  {
    task_id: 'task-002',
    mode: 'bounded-reproduction',
    title: 'SAGDFN Table 2 Reproduction',
    status: 'completed',
    stage: 'analysis',
    updated_at: new Date(Date.now() - 3600000).toISOString(),
    termination_reason: 'completed',
  },
  {
    task_id: 'task-003',
    mode: 'bounded-discovery',
    title: 'GNN for Molecular Property Prediction',
    status: 'failed',
    stage: 'paper-processing',
    updated_at: new Date(Date.now() - 7200000).toISOString(),
    termination_reason: 'paper_processing_error',
  },
];

const mockArtifactsPreview: ArtifactPreview[] = [
  { artifact_id: 'a1', artifact_type: 'table', display_title: 'Paper Summary', preview_format: 'markdown', preview_ref: '/artifacts/a1/content' },
  { artifact_id: 'a2', artifact_type: 'figure', display_title: 'Attention Heatmap', preview_format: 'svg', preview_ref: '/artifacts/a2/content' },
];

const mockTaskDetail: TaskReadModel = {
  identity: {
    task_id: 'task-001',
    mode: 'bounded-discovery',
    created_at: new Date(Date.now() - 86400000).toISOString(),
    updated_at: new Date().toISOString(),
  },
  lifecycle: {
    status: 'running',
    stage: 'literature-search',
    termination_reason: null,
    active_gate: null,
  },
  input_summary: {
    title: 'Attention Mechanism Survey',
    brief: 'Survey of attention mechanisms in deep learning for computer vision tasks',
    seed_inputs: ['attention-is-all-you-need.pdf', 'vit-paper.pdf'],
    target_inputs: [],
  },
  progress_summary: {
    current_checkpoint: 'literature-search',
    milestones: [
      { id: 'm1', name: 'Paper Collection', status: 'completed', timestamp: new Date(Date.now() - 72000000).toISOString() },
      { id: 'm2', name: 'Literature Search', status: 'in_progress', timestamp: new Date().toISOString() },
    ],
    recent_events: [
      { id: 'e1', message: 'Found 15 relevant papers', timestamp: new Date(Date.now() - 3600000).toISOString() },
    ],
    artifact_counts: { tables: 1, reports: 0, figures: 2 },
  },
  result_summary: {
    result_brief: null,
    termination_reason: null,
    recent_artifacts: mockArtifactsPreview,
    error_summary: null,
  },
};

const mockArtifacts: ArtifactListItem[] = [
  { artifact_id: 'a1', artifact_type: 'table', display_title: 'Paper Summary', preview_format: 'markdown' },
  { artifact_id: 'a2', artifact_type: 'figure', display_title: 'Attention Heatmap', preview_format: 'svg' },
  { artifact_id: 'a3', artifact_type: 'report', display_title: 'Survey Draft', preview_format: 'markdown' },
];

const mockExecutionContext: ExecutionContextSummary = {
  workspace: {
    workspace_id: 'ws-001',
    workspace_label: 'research-workspace',
    project_dir: '/home/user/research',
  },
  session: {
    session_status: 'active',
    connected: true,
    recoverable: true,
  },
  container: {
    container_label: 'research-container',
    ssh_available: true,
    environment_status: 'ready',
  },
  resource_snapshot: {
    gpu: 45,
    cpu: 32,
    memory: 68,
    disk: 23,
  },
};

const mockHealth: SystemHealth = {
  api_status: 'ok',
  ssh_available: true,
  workspace_ready: true,
};

// Mock API handlers
export function mockGetHealth(): SystemHealth {
  return mockHealth;
}

export function mockGetTasks(): TaskListItem[] {
  return mockTasks;
}

export function mockGetRunningTasks(): TaskListItem[] {
  return mockTasks.filter(t => t.status === 'running');
}

export function mockGetRecentTasks(): TaskListItem[] {
  return mockTasks.filter(t => t.status !== 'running');
}

export function mockGetTask(taskId: string): TaskReadModel {
  if (taskId === 'task-001') {
    return mockTaskDetail;
  }
  throw new Error('Task not found');
}

export function mockGetRecentArtifacts(): ArtifactListItem[] {
  return mockArtifacts;
}

export function mockGetArtifactContent(artifactId: string): { content: string; format: string } {
  if (artifactId === 'a1') {
    return {
      content: '# Paper Summary\n\n| Paper | Year | Venue |\n|-------|------|-------|\n| Attention Is All You Need | 2017 | NeurIPS |\n| ViT | 2021 | ICLR |',
      format: 'markdown',
    };
  }
  if (artifactId === 'a2') {
    return {
      content: '<svg width="100" height="100"><circle cx="50" cy="50" r="40" fill="blue"/></svg>',
      format: 'svg',
    };
  }
  return { content: 'Content not available', format: 'text' };
}

export function mockGetExecutionContext(): ExecutionContextSummary {
  return mockExecutionContext;
}