import { describe, expect, it } from 'vitest';
import {
  createCodeServerSession,
  createTerminalSession,
  deleteCodeServerSession,
  deleteTerminalSession,
  getCodeServerStatus,
  getTerminalSession,
} from './api/endpoints';
import {
  mockCreateCodeServerSession,
  mockCreateTerminalSession,
  mockDeleteCodeServerSession,
  mockDeleteTerminalSession,
  mockGetCodeServerStatus,
  mockGetTerminalSession,
} from './api/mock';
import type { CodeServerStatus, TerminalSession } from './types';

describe('terminal contract smoke test', () => {
  it('preserves terminal session and code-server shapes', () => {
    const terminalSessionLoaders: Array<() => Promise<TerminalSession>> = [
      () => getTerminalSession('env-1'),
      () => createTerminalSession('env-1'),
      deleteTerminalSession,
    ];
    const mockTerminalSessionLoaders: Array<() => TerminalSession> = [
      () => mockGetTerminalSession('env-1'),
      () => mockCreateTerminalSession('env-1'),
      mockDeleteTerminalSession,
    ];
    const codeServerLoaders: Array<() => Promise<CodeServerStatus>> = [
      () => getCodeServerStatus('env-1'),
      () => createCodeServerSession('env-1'),
      deleteCodeServerSession,
    ];
    const mockCodeServerLoaders: Array<() => CodeServerStatus> = [
      () => mockGetCodeServerStatus('env-1'),
      () => mockCreateCodeServerSession('env-1'),
      mockDeleteCodeServerSession,
    ];

    const terminalSessionStatusValues: TerminalSession['status'][] = [
      'idle',
      'starting',
      'running',
      'stopping',
      'failed',
    ];
    const terminalSessionContract: TerminalSession = {
      session_id: 'term-1',
      provider: 'pty',
      target_kind: 'environment-ssh',
      environment_id: 'env-1',
      environment_alias: 'gpu-lab',
      working_directory: '/workspace/project-a',
      status: 'running',
      created_at: '2026-04-13T16:00:00Z',
      started_at: '2026-04-13T16:00:01Z',
      closed_at: null,
      terminal_ws_url: 'ws://lab.internal:5173/terminal/session/term-1/ws?token=test-token',
      detail: null,
    };

    const codeServerStatuses: CodeServerStatus['status'][] = ['starting', 'ready', 'unavailable'];
    const codeServerContract: CodeServerStatus = {
      status: 'ready',
      environment_id: 'env-1',
      environment_alias: 'gpu-lab',
      workspace_dir: '/workspace/project-a',
      detail: null,
      managed: true,
    };

    expect(terminalSessionLoaders).toHaveLength(3);
    expect(mockTerminalSessionLoaders).toHaveLength(3);
    expect(codeServerLoaders).toHaveLength(3);
    expect(mockCodeServerLoaders).toHaveLength(3);
    expect(terminalSessionStatusValues).toEqual([
      'idle',
      'starting',
      'running',
      'stopping',
      'failed',
    ]);
    expect(new URL(terminalSessionContract.terminal_ws_url ?? '').host).toBe('lab.internal:5173');
    expect(new URL(terminalSessionContract.terminal_ws_url ?? '').pathname).toBe('/terminal/session/term-1/ws');
    expect(terminalSessionContract.status).toBe('running');
    expect(codeServerStatuses).toEqual(['starting', 'ready', 'unavailable']);
    expect(codeServerContract.managed).toBe(true);
  });
});
