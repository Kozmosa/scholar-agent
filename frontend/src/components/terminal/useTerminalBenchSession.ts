import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  createTerminalSession,
  deleteTerminalSession,
  getTerminalSession,
} from '../../api';
import type { TerminalSessionStatus } from '../../types';

const terminalSessionQueryKey = ['terminal-session'] as const;

export interface TerminalBenchSessionState {
  sessionId: string | null;
  status: TerminalSessionStatus;
  terminalWsUrl: string | null;
  detail: string | null;
  loadError: string | null;
  isLoading: boolean;
  isStarting: boolean;
  isStopping: boolean;
  canStart: boolean;
  canStop: boolean;
  onStart: () => void;
  onStop: () => void;
  onTerminalDisconnected: () => void;
}

function getErrorMessage(error: unknown): string | null {
  return error instanceof Error ? error.message : null;
}

export function useTerminalBenchSession(): TerminalBenchSessionState {
  const queryClient = useQueryClient();
  const terminalQuery = useQuery({
    queryKey: terminalSessionQueryKey,
    queryFn: getTerminalSession,
  });

  const startMutation = useMutation({
    mutationFn: createTerminalSession,
    onSuccess: (session) => {
      queryClient.setQueryData(terminalSessionQueryKey, session);
    },
  });

  const stopMutation = useMutation({
    mutationFn: deleteTerminalSession,
    onSuccess: (session) => {
      queryClient.setQueryData(terminalSessionQueryKey, session);
    },
  });

  const session = terminalQuery.data;
  const status = session?.status ?? 'idle';
  const loadError = getErrorMessage(terminalQuery.error);
  const mutationError = getErrorMessage(startMutation.error) ?? getErrorMessage(stopMutation.error);
  const detail = mutationError ?? session?.detail ?? null;
  const isLoading = terminalQuery.isLoading;
  const isStarting = startMutation.isPending;
  const isStopping = stopMutation.isPending;
  const canStart =
    !isLoading &&
    loadError === null &&
    !isStarting &&
    !isStopping &&
    status !== 'running' &&
    status !== 'starting';
  const canStop =
    !isLoading &&
    loadError === null &&
    !isStarting &&
    !isStopping &&
    status !== 'idle' &&
    status !== 'stopping';

  return {
    sessionId: session?.session_id ?? null,
    status,
    terminalWsUrl: session?.terminal_ws_url ?? null,
    detail,
    loadError,
    isLoading,
    isStarting,
    isStopping,
    canStart,
    canStop,
    onStart: () => startMutation.mutate(),
    onStop: () => stopMutation.mutate(),
    onTerminalDisconnected: () => {
      queryClient.invalidateQueries({ queryKey: terminalSessionQueryKey });
    },
  };
}
