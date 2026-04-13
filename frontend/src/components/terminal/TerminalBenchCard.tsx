import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  createTerminalSession,
  deleteTerminalSession,
  getTerminalSession,
} from '../../api';
import type { TerminalSessionStatus } from '../../types';

const statusLabel: Record<TerminalSessionStatus, string> = {
  idle: 'Idle',
  starting: 'Starting',
  running: 'Running',
  stopping: 'Stopping',
  failed: 'Failed',
};

function TerminalBenchCard() {
  const queryClient = useQueryClient();
  const terminalQuery = useQuery({
    queryKey: ['terminal-session'],
    queryFn: getTerminalSession,
  });

  const startMutation = useMutation({
    mutationFn: createTerminalSession,
    onSuccess: (session) => {
      queryClient.setQueryData(['terminal-session'], session);
    },
  });

  const stopMutation = useMutation({
    mutationFn: deleteTerminalSession,
    onSuccess: (session) => {
      queryClient.setQueryData(['terminal-session'], session);
    },
  });

  const session = terminalQuery.data;
  const status = session?.status ?? 'idle';
  const isStarting = startMutation.isPending;
  const isStopping = stopMutation.isPending;
  const canStart = !isStarting && !isStopping && status !== 'running' && status !== 'starting';
  const canStop = !isStarting && !isStopping && status !== 'idle' && status !== 'stopping';
  const detail = startMutation.error?.message ?? stopMutation.error?.message ?? session?.detail;

  return (
    <section className="space-y-4 rounded-xl border border-gray-200 bg-gray-50 p-5">
      <div className="space-y-1">
        <h2 className="text-lg font-medium text-gray-900">Terminal Bench</h2>
        <p className="text-sm text-gray-600">
          Launch the minimal terminal shell backed by the daemon-host terminal session API.
        </p>
      </div>

      <div className="flex flex-wrap items-center gap-3 text-sm text-gray-700">
        <span className="font-medium text-gray-900">Status: {statusLabel[status]}</span>
        <button
          type="button"
          onClick={() => startMutation.mutate()}
          disabled={!canStart}
          className="rounded-md bg-[var(--accent)] px-3 py-1.5 font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isStarting ? 'Starting…' : 'Start terminal'}
        </button>
        <button
          type="button"
          onClick={() => stopMutation.mutate()}
          disabled={!canStop}
          className="rounded-md border border-gray-300 bg-white px-3 py-1.5 font-medium text-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isStopping ? 'Stopping…' : 'Stop terminal'}
        </button>
      </div>

      {terminalQuery.isLoading ? (
        <p className="text-sm text-gray-500">Loading terminal session...</p>
      ) : null}

      {terminalQuery.isError ? (
        <p className="text-sm text-red-700">Unable to load terminal session.</p>
      ) : null}

      {detail ? <p className="text-sm text-gray-600">Detail: {detail}</p> : null}

      {status === 'running' && session?.terminal_url ? (
        <iframe
          title="Terminal Bench session"
          src={session.terminal_url}
          className="h-[480px] w-full rounded-lg border border-gray-300 bg-white"
        />
      ) : null}
    </section>
  );
}

export default TerminalBenchCard;
