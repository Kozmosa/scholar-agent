import { api } from './client';
import type { SystemHealth } from '../types';
import { mockGetHealth } from './mock';

const USE_MOCK = import.meta.env.DEV;

export const getHealth = (): Promise<SystemHealth> =>
  USE_MOCK ? Promise.resolve(mockGetHealth()) : api.get<SystemHealth>('/health');
