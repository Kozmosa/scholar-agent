import { describe, expect, it } from 'vitest';
import {
  createTerminalSession,
  deleteTerminalSession,
  getCodeServerStatus,
  getTerminalSession,
} from './api/endpoints';
import {
  mockCreateTerminalSession,
  mockDeleteTerminalSession,
  mockGetCodeServerStatus,
  mockGetTerminalSession,
} from './api/mock';
import type { CodeServerStatus, TerminalSession } from './types';

describe('terminal contract smoke test', () => {
  it('preserves terminal session and code-server shapes', () => {
    const terminalSessionLoaders: Array<() => Promise<TerminalSession>> = [
      getTerminalSession,
      createTerminalSession,
      deleteTerminalSession,
    ];
    const mockTerminalSessionLoaders: Array<() => TerminalSession> = [
      mockGetTerminalSession,
      mockCreateTerminalSession,
      mockDeleteTerminalSession,
    ];
    const codeServerLoader: () => Promise<CodeServerStatus> = getCodeServerStatus;
    const mockCodeServerLoader: () => CodeServerStatus = mockGetCodeServerStatus;

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
      target_kind: 'daemon-host',
      status: 'running',
      created_at: '2026-04-13T16:00:00Z',
      started_at: '2026-04-13T16:00:01Z',
      closed_at: null,
      terminal_ws_url: 'ws://127.0.0.1:8000/terminal/session/term-1/ws?token=test-token',
      detail: null,
    };

    const codeServerStatuses: CodeServerStatus['status'][] = ['starting', 'ready', 'unavailable'];
    const codeServerContract: CodeServerStatus = {
      status: 'ready',
      workspace_dir: '/workspace/project-a',
      detail: null,
      managed: true,
    };

    expect(terminalSessionLoaders).toHaveLength(3);
    expect(mockTerminalSessionLoaders).toHaveLength(3);
    expect(codeServerLoader).toBeTypeOf('function');
    expect(mockCodeServerLoader).toBeTypeOf('function');
    expect(terminalSessionStatusValues).toEqual([
      'idle',
      'starting',
      'running',
      'stopping',
      'failed',
    ]);
    expect(terminalSessionContract.status).toBe('running');
    expect(codeServerStatuses).toEqual(['starting', 'ready', 'unavailable']);
    expect(codeServerContract.managed).toBe(true);
  });
});
