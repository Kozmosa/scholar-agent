import { beforeEach, describe, expect, it, vi } from 'vitest';
import { resetMockTerminalSession } from './mock';

beforeEach(() => {
  vi.resetModules();
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
  resetMockTerminalSession();
});

describe('api endpoints', () => {
  it('uses the mock transport only when VITE_USE_MOCK is true', async () => {
    vi.stubEnv('VITE_USE_MOCK', 'true');

    const { createTerminalSession, getTerminalSession } = await import('./endpoints');
    const session = await getTerminalSession('env-localhost');
    const created = await createTerminalSession('env-localhost');

    expect(session.status).toBe('idle');
    expect(created.status).toBe('running');
    expect(created.terminal_ws_url).toBe(
      'ws://127.0.0.1:8000/terminal/session/mock-terminal-session-env-localhost/ws?token=mock-token'
    );
  });

  it('uses the real api client when VITE_USE_MOCK is false', async () => {
    vi.stubEnv('VITE_USE_MOCK', 'false');
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ status: 'ok' }), {
        status: 200,
        headers: {
          'content-type': 'application/json',
        },
      })
    );
    vi.stubGlobal('fetch', fetchMock);

    const { getHealth } = await import('./endpoints');
    await expect(getHealth()).resolves.toEqual({ status: 'ok' });
    expect(fetchMock).toHaveBeenCalledWith('/api/health', expect.any(Object));
  });
});
