const API_BASE = '/api';
const API_KEY = import.meta.env.VITE_AINRF_API_KEY?.trim() ?? '';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: unknown;
}

class ApiError extends Error {
  status: number;
  data?: unknown;
  path: string;

  constructor(message: string, status: number, path: string, data?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.path = path;
    this.data = data;
  }
}

function getErrorDetail(data: unknown): string | null {
  if (typeof data === 'string') {
    return data.trim() || null;
  }

  if (!data || typeof data !== 'object') {
    return null;
  }

  const record = data as Record<string, unknown>;
  for (const key of ['detail', 'message', 'error', 'title', 'reason']) {
    const value = record[key];
    if (typeof value === 'string' && value.trim()) {
      return value.trim();
    }
  }

  return null;
}

async function parseResponseBody(response: Response): Promise<unknown> {
  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get('content-type') ?? '';
  const rawBody = await response.text().catch(() => '');

  if (!rawBody) {
    return null;
  }

  if (contentType.includes('application/json')) {
    try {
      return JSON.parse(rawBody) as unknown;
    } catch {
      return rawBody;
    }
  }

  return rawBody;
}

function createErrorMessage(path: string, response: Response, data: unknown): string {
  const detail = getErrorDetail(data);
  const statusLabel = response.statusText.trim() || 'Unknown Error';
  const baseMessage = `Request to ${path} failed with ${response.status} ${statusLabel}`;
  return detail ? `${baseMessage}: ${detail}` : baseMessage;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const url = `${API_BASE}${path}`;
  const headers = new Headers({
    'Content-Type': 'application/json',
  });

  if (API_KEY) {
    headers.set('X-API-Key', API_KEY);
  }

  const init: RequestInit = {
    method: options.method ?? 'GET',
    headers,
  };

  if (options.body !== undefined) {
    init.body = JSON.stringify(options.body);
  }

  const response = await fetch(url, init);

  if (!response.ok) {
    const data = await parseResponseBody(response);
    throw new ApiError(createErrorMessage(path, response, data), response.status, path, data);
  }

  const data = await parseResponseBody(response);
  return data as T;
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body: unknown) => request<T>(path, { method: 'POST', body }),
  put: <T>(path: string, body: unknown) => request<T>(path, { method: 'PUT', body }),
  patch: <T>(path: string, body: unknown) => request<T>(path, { method: 'PATCH', body }),
  delete: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
};

export { ApiError };
