import { api } from './client';
import type {
  TaskReadModel,
  TaskListItem,
  ArtifactPreview,
  ArtifactListItem,
  ExecutionContextSummary,
  SystemHealth,
} from '../types';

// Health check
export const getHealth = () => api.get<SystemHealth>('/health');

// Tasks
export const getTasks = () => api.get<TaskListItem[]>('/tasks');
export const getRunningTasks = () => api.get<TaskListItem[]>('/tasks/running');
export const getRecentTasks = () => api.get<TaskListItem[]>('/tasks/recent');
export const getTask = (taskId: string) => api.get<TaskReadModel>(`/tasks/${taskId}`);

// Artifacts
export const getRecentArtifacts = () => api.get<ArtifactListItem[]>('/artifacts/recent');
export const getArtifact = (artifactId: string) => api.get<ArtifactPreview>(`/artifacts/${artifactId}`);
export const getArtifactContent = (artifactId: string) =>
  api.get<{ content: string; format: string }>(`/artifacts/${artifactId}/content`);

// Execution context
export const getExecutionContext = () => api.get<ExecutionContextSummary>('/context');
export const getResourceSnapshot = () => api.get<ExecutionContextSummary['resource_snapshot']>('/context/resources');