import { api } from './client';
import type {
  CodeServerStatus,
  EnvironmentCreateRequest,
  EnvironmentListResponse,
  EnvironmentRecord,
  EnvironmentUpdateRequest,
  SystemHealth,
  TerminalSession,
} from '../types';
import {
  mockCreateEnvironment,
  mockCreateTerminalSession,
  mockDeleteEnvironment,
  mockDeleteTerminalSession,
  mockDetectEnvironment,
  mockGetCodeServerStatus,
  mockGetEnvironments,
  mockGetHealth,
  mockGetEnvironment,
  mockGetTerminalSession,
  mockUpdateEnvironment,
} from './mock';

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

export const getHealth = (): Promise<SystemHealth> =>
  USE_MOCK ? Promise.resolve(mockGetHealth()) : api.get<SystemHealth>('/health');

export const getTerminalSession = (): Promise<TerminalSession> =>
  USE_MOCK
    ? Promise.resolve(mockGetTerminalSession())
    : api.get<TerminalSession>('/terminal/session');

export const createTerminalSession = (): Promise<TerminalSession> =>
  USE_MOCK
    ? Promise.resolve(mockCreateTerminalSession())
    : api.post<TerminalSession>('/terminal/session', {});

export const deleteTerminalSession = (): Promise<TerminalSession> =>
  USE_MOCK
    ? Promise.resolve(mockDeleteTerminalSession())
    : api.delete<TerminalSession>('/terminal/session');

export const getCodeServerStatus = (): Promise<CodeServerStatus> =>
  USE_MOCK
    ? Promise.resolve(mockGetCodeServerStatus())
    : api.get<CodeServerStatus>('/code/status');

export const getEnvironments = (): Promise<EnvironmentListResponse> =>
  USE_MOCK ? Promise.resolve(mockGetEnvironments()) : api.get<EnvironmentListResponse>('/environments');

export const getEnvironment = (environmentId: string): Promise<EnvironmentRecord> =>
  USE_MOCK
    ? Promise.resolve(mockGetEnvironment(environmentId))
    : api.get<EnvironmentRecord>(`/environments/${environmentId}`);

export const createEnvironment = (
  payload: EnvironmentCreateRequest
): Promise<EnvironmentRecord> =>
  USE_MOCK
    ? Promise.resolve(mockCreateEnvironment(payload))
    : api.post<EnvironmentRecord>('/environments', payload);

export const updateEnvironment = (
  environmentId: string,
  payload: EnvironmentUpdateRequest
): Promise<EnvironmentRecord> =>
  USE_MOCK
    ? Promise.resolve(mockUpdateEnvironment(environmentId, payload))
    : api.patch<EnvironmentRecord>(`/environments/${environmentId}`, payload);

export const deleteEnvironment = (environmentId: string): Promise<void> =>
  USE_MOCK
    ? Promise.resolve(mockDeleteEnvironment(environmentId))
    : api.delete<void>(`/environments/${environmentId}`);

export const detectEnvironment = (environmentId: string): Promise<EnvironmentRecord> =>
  USE_MOCK
    ? Promise.resolve(mockDetectEnvironment(environmentId))
    : api.post<EnvironmentRecord>(`/environments/${environmentId}/detect`, {});
