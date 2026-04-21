import { beforeEach, describe, expect, it, vi } from 'vitest';

beforeEach(() => {
  vi.resetModules();
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
});

describe('api client', () => {
  it('injects the configured API key header', async () => {
    vi.stubEnv('VITE_AINRF_API_KEY', 'secret-key');
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ status: 'ok' }), {
        status: 200,
        headers: {
          'content-type': 'application/json',
        },
      })
    );
    vi.stubGlobal('fetch', fetchMock);

    const { api } = await import('./client');
    await expect(api.get<{ status: string }>('/health')).resolves.toEqual({ status: 'ok' });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    const init = fetchMock.mock.calls[0]?.[1] as RequestInit | undefined;
    expect(init).toBeDefined();
    expect(new Headers(init?.headers).get('X-API-Key')).toBe('secret-key');
  });

  it('surfaces server error details in ApiError', async () => {
    const response = {
      ok: false,
      status: 503,
      statusText: 'Service Unavailable',
      headers: new Headers({
        'content-type': 'application/json',
      }),
      text: async () => JSON.stringify({ detail: 'terminal unavailable' }),
    } as Response;
    const fetchMock = vi.fn().mockResolvedValue(response);
    vi.stubGlobal('fetch', fetchMock);

    const { ApiError, api } = await import('./client');

    try {
      await api.get('/terminal/session');
      throw new Error('expected request to fail');
    } catch (error: unknown) {
      expect(error).toBeInstanceOf(ApiError);
      expect(error).toMatchObject({
        name: 'ApiError',
        status: 503,
        path: '/terminal/session',
        data: {
          detail: 'terminal unavailable',
        },
      });
      expect((error as Error).message).toBe(
        'Request to /terminal/session failed with 503 Service Unavailable: terminal unavailable'
      );
    }
  });
});
