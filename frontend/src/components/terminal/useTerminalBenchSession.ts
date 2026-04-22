import { useEffect, useRef } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  createTerminalSession,
  deleteTerminalSession,
  getTerminalSession,
} from '../../api';
import type { EnvironmentRecord, TerminalSession, TerminalSessionStatus } from '../../types';

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

export function useTerminalBenchSession(
  selectedEnvironment: EnvironmentRecord | null
): TerminalBenchSessionState {
  const queryClient = useQueryClient();
  const selectedEnvironmentId = selectedEnvironment?.id ?? null;
  const previousEnvironmentIdRef = useRef<string | null>(selectedEnvironmentId);
  const terminalQuery = useQuery({
    queryKey: [...terminalSessionQueryKey, selectedEnvironmentId],
    queryFn: () => {
      if (selectedEnvironmentId === null) {
        return Promise.resolve<TerminalSession>({
          session_id: null,
          provider: 'pty',
          target_kind: 'daemon-host',
          environment_id: null,
          environment_alias: null,
          working_directory: null,
          status: 'idle',
          created_at: null,
          started_at: null,
          closed_at: null,
          terminal_ws_url: null,
          detail: null,
        });
      }
      return getTerminalSession(selectedEnvironmentId);
    },
  });

  const startMutation = useMutation({
    mutationFn: (environmentId: string) => createTerminalSession(environmentId),
    onSuccess: (session, environmentId) => {
      queryClient.setQueryData([...terminalSessionQueryKey, environmentId], session);
    },
  });

  const stopMutation = useMutation({
    mutationFn: deleteTerminalSession,
    onSuccess: (session) => {
      if (selectedEnvironmentId !== null) {
        queryClient.setQueryData([...terminalSessionQueryKey, selectedEnvironmentId], session);
      }
    },
  });

  useEffect(() => {
    const previousEnvironmentId = previousEnvironmentIdRef.current;
    if (
      previousEnvironmentId !== null &&
      previousEnvironmentId !== selectedEnvironmentId &&
      selectedEnvironmentId !== null
    ) {
      const previousSession = queryClient.getQueryData<TerminalSession>([
        ...terminalSessionQueryKey,
        previousEnvironmentId,
      ]);
      if (previousSession?.status === 'running' || previousSession?.status === 'starting') {
        startMutation.mutate(selectedEnvironmentId);
      }
    }
    previousEnvironmentIdRef.current = selectedEnvironmentId;
  }, [queryClient, selectedEnvironmentId, startMutation]);

  const session = terminalQuery.data;
  const status = session?.status ?? 'idle';
  const loadError = getErrorMessage(terminalQuery.error);
  const mutationError = getErrorMessage(startMutation.error) ?? getErrorMessage(stopMutation.error);
  const detail = mutationError ?? session?.detail ?? null;
  const isLoading = terminalQuery.isLoading;
  const isStarting = startMutation.isPending;
  const isStopping = stopMutation.isPending;
  const canStart =
    selectedEnvironmentId !== null &&
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
    onStart: () => {
      if (selectedEnvironmentId !== null) {
        startMutation.mutate(selectedEnvironmentId);
      }
    },
    onStop: () => stopMutation.mutate(),
    onTerminalDisconnected: () => {
      queryClient.invalidateQueries({ queryKey: terminalSessionQueryKey });
    },
  };
}
