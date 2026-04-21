vi.mock('./TerminalSessionConsole', () => ({
  default: () => <div data-testid="terminal-console" />,
}));

import { fireEvent, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import TerminalBenchCard from './TerminalBenchCard';
import type { EnvironmentRecord, TerminalSession } from '../../types';
import { renderWithProviders } from '../../test/render';
import {
  createTerminalSession,
  deleteTerminalSession,
  getTerminalSession,
} from '../../api';

vi.mock('../../api', () => ({
  createTerminalSession: vi.fn(),
  deleteTerminalSession: vi.fn(),
  getTerminalSession: vi.fn(),
}));

const mockGetTerminalSession = vi.mocked(getTerminalSession);
const mockCreateTerminalSession = vi.mocked(createTerminalSession);
const mockDeleteTerminalSession = vi.mocked(deleteTerminalSession);

const idleSession: TerminalSession = {
  session_id: null,
  provider: 'pty',
  target_kind: 'daemon-host',
  status: 'idle',
  created_at: null,
  started_at: null,
  closed_at: null,
  terminal_ws_url: null,
  detail: null,
};

const runningSession: TerminalSession = {
  session_id: 'term-1',
  provider: 'pty',
  target_kind: 'daemon-host',
  status: 'running',
  created_at: '2026-04-21T00:00:00Z',
  started_at: '2026-04-21T00:00:01Z',
  closed_at: null,
  terminal_ws_url: 'ws://127.0.0.1:8000/terminal/session/term-1/ws?token=test-token',
  detail: null,
};

const selectedEnvironment: EnvironmentRecord = {
  id: 'env-1',
  alias: 'gpu-lab',
  display_name: 'GPU Lab',
  description: null,
  is_seed: false,
  tags: [],
  host: 'gpu.example.com',
  port: 22,
  user: 'root',
  auth_kind: 'ssh_key',
  identity_file: null,
  proxy_jump: null,
  proxy_command: null,
  ssh_options: {},
  default_workdir: '/workspace/project',
  preferred_python: null,
  preferred_env_manager: null,
  preferred_runtime_notes: null,
  created_at: '2026-04-21T00:00:00Z',
  updated_at: '2026-04-21T00:00:00Z',
  latest_detection: null,
};

beforeEach(() => {
  mockGetTerminalSession.mockReset();
  mockCreateTerminalSession.mockReset();
  mockDeleteTerminalSession.mockReset();
});

describe('TerminalBenchCard', () => {
  it('renders the idle state from the backend', async () => {
    mockGetTerminalSession.mockResolvedValue(idleSession);

    renderWithProviders(<TerminalBenchCard selectedEnvironment={selectedEnvironment} />);

    expect(await screen.findByText('Status: Idle')).toBeInTheDocument();
    await waitFor(() => expect(screen.getByRole('button', { name: 'Start terminal' })).not.toBeDisabled());
    expect(screen.getByRole('button', { name: 'Stop terminal' })).toBeDisabled();
    expect(screen.getByText('No terminal session is running.')).toBeInTheDocument();
    expect(screen.getByTestId('terminal-console')).toBeInTheDocument();
  });

  it('starts a terminal session and shows the console', async () => {
    mockGetTerminalSession.mockResolvedValue(idleSession);
    mockCreateTerminalSession.mockResolvedValue(runningSession);

    renderWithProviders(<TerminalBenchCard selectedEnvironment={selectedEnvironment} />);

    await screen.findByText('Status: Idle');
    await waitFor(() => expect(screen.getByRole('button', { name: 'Start terminal' })).not.toBeDisabled());
    fireEvent.click(screen.getByRole('button', { name: 'Start terminal' }));

    await waitFor(() => expect(mockCreateTerminalSession).toHaveBeenCalledTimes(1));
    expect(await screen.findByText('Status: Running')).toBeInTheDocument();
    expect(screen.getByTestId('terminal-console')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Stop terminal' })).toBeEnabled();
  });

  it('stops a running terminal session and returns to idle state', async () => {
    mockGetTerminalSession.mockResolvedValue(runningSession);
    mockDeleteTerminalSession.mockResolvedValue(idleSession);

    renderWithProviders(<TerminalBenchCard selectedEnvironment={selectedEnvironment} />);

    expect(await screen.findByText('Status: Running')).toBeInTheDocument();
    expect(screen.getByTestId('terminal-console')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Stop terminal' }));

    await waitFor(() => expect(mockDeleteTerminalSession).toHaveBeenCalledTimes(1));
    expect(await screen.findByText('Status: Idle')).toBeInTheDocument();
    expect(screen.getByTestId('terminal-console')).toBeInTheDocument();
  });

  it('surfaces backend load errors', async () => {
    mockGetTerminalSession.mockRejectedValue(new Error('backend offline'));

    renderWithProviders(<TerminalBenchCard selectedEnvironment={selectedEnvironment} />);

    expect(await screen.findByText('Load error: backend offline')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start terminal' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'Stop terminal' })).toBeDisabled();
  });

  it('requires a selected environment before enabling the terminal', async () => {
    mockGetTerminalSession.mockResolvedValue(idleSession);

    renderWithProviders(<TerminalBenchCard selectedEnvironment={null} />);

    expect(await screen.findByText('Status: Idle')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start terminal' })).toBeDisabled();
    expect(screen.getByText('Select an environment before starting the terminal session.')).toBeInTheDocument();
  });
});
