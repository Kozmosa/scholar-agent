import { api } from './client';
import type { SystemHealth, TerminalSession } from '../types';
import {
  mockCreateTerminalSession,
  mockDeleteTerminalSession,
  mockGetHealth,
  mockGetTerminalSession,
} from './mock';

const USE_MOCK = import.meta.env.DEV;

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
