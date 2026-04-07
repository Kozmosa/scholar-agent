import { api } from './client';
import type {
  TaskReadModel,
  TaskListItem,
  ArtifactPreview,
  ArtifactListItem,
  ExecutionContextSummary,
  SystemHealth,
} from '../types';
import {
  mockGetHealth,
  mockGetTasks,
  mockGetRunningTasks,
  mockGetRecentTasks,
  mockGetTask,
  mockGetRecentArtifacts,
  mockGetArtifactContent,
  mockGetExecutionContext,
} from './mock';

// Use mock data in development
const USE_MOCK = import.meta.env.DEV;

// Health check
export const getHealth = (): Promise<SystemHealth> =>
  USE_MOCK ? Promise.resolve(mockGetHealth()) : api.get<SystemHealth>('/health');

// Tasks
export const getTasks = (): Promise<TaskListItem[]> =>
  USE_MOCK ? Promise.resolve(mockGetTasks()) : api.get<TaskListItem[]>('/tasks');

export const getRunningTasks = (): Promise<TaskListItem[]> =>
  USE_MOCK ? Promise.resolve(mockGetRunningTasks()) : api.get<TaskListItem[]>('/tasks/running');

export const getRecentTasks = (): Promise<TaskListItem[]> =>
  USE_MOCK ? Promise.resolve(mockGetRecentTasks()) : api.get<TaskListItem[]>('/tasks/recent');

export const getTask = (taskId: string): Promise<TaskReadModel> =>
  USE_MOCK ? Promise.resolve(mockGetTask(taskId)) : api.get<TaskReadModel>(`/tasks/${taskId}`);

// Artifacts
export const getRecentArtifacts = (): Promise<ArtifactListItem[]> =>
  USE_MOCK ? Promise.resolve(mockGetRecentArtifacts()) : api.get<ArtifactListItem[]>('/artifacts/recent');

export const getArtifact = (artifactId: string): Promise<ArtifactPreview> =>
  api.get<ArtifactPreview>(`/artifacts/${artifactId}`);

export const getArtifactContent = (artifactId: string): Promise<{ content: string; format: string }> =>
  USE_MOCK
    ? Promise.resolve(mockGetArtifactContent(artifactId))
    : api.get<{ content: string; format: string }>(`/artifacts/${artifactId}/content`);

// Execution context
export const getExecutionContext = (): Promise<ExecutionContextSummary> =>
  USE_MOCK
    ? Promise.resolve(mockGetExecutionContext())
    : api.get<ExecutionContextSummary>('/context');

export const getResourceSnapshot = (): Promise<ExecutionContextSummary['resource_snapshot']> =>
  USE_MOCK
    ? Promise.resolve(mockGetExecutionContext().resource_snapshot)
    : api.get<ExecutionContextSummary['resource_snapshot']>('/context/resources');