import { useEffect, useRef, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  createCodeServerSession,
  deleteCodeServerSession,
  getCodeServerStatus,
} from '../../api';
import { useT } from '../../i18n';
import type { CodeServerStatus, EnvironmentRecord } from '../../types';

const codeServerQueryKey = ['code-server-status'] as const;

interface Props {
  selectedEnvironment: EnvironmentRecord | null;
}

function CodeServerCard({ selectedEnvironment }: Props) {
  const t = useT();
  const queryClient = useQueryClient();
  const selectedEnvironmentId = selectedEnvironment?.id ?? null;
  const previousEnvironmentIdRef = useRef<string | null>(selectedEnvironmentId);
  const [iframeRevision, setIframeRevision] = useState(0);

  const codeQuery = useQuery({
    queryKey: [...codeServerQueryKey, selectedEnvironmentId],
    enabled: selectedEnvironmentId !== null,
    queryFn: () => getCodeServerStatus(selectedEnvironmentId ?? undefined),
  });

  const ensureMutation = useMutation({
    mutationFn: (environmentId: string) => createCodeServerSession(environmentId),
    onSuccess: (status, environmentId) => {
      queryClient.setQueryData([...codeServerQueryKey, environmentId], status);
      setIframeRevision((value) => value + 1);
    },
  });

  const stopMutation = useMutation({
    mutationFn: deleteCodeServerSession,
    onSuccess: (status) => {
      if (selectedEnvironmentId !== null) {
        queryClient.setQueryData([...codeServerQueryKey, selectedEnvironmentId], status);
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
      const previousStatus = queryClient.getQueryData<CodeServerStatus>([
        ...codeServerQueryKey,
        previousEnvironmentId,
      ]);
      if (previousStatus?.status === 'ready' || previousStatus?.status === 'starting') {
        ensureMutation.mutate(selectedEnvironmentId);
      }
    }
    previousEnvironmentIdRef.current = selectedEnvironmentId;
  }, [ensureMutation, queryClient, selectedEnvironmentId]);

  const status = codeQuery.data?.status;
  const workspaceDir =
    codeQuery.data?.workspace_dir ??
    selectedEnvironment?.default_workdir ??
    t('common.notConfigured');
  const queryError = codeQuery.error instanceof Error ? codeQuery.error.message : null;
  const mutationError =
    (ensureMutation.error instanceof Error ? ensureMutation.error.message : null) ??
    (stopMutation.error instanceof Error ? stopMutation.error.message : null);
  const detail = mutationError ?? queryError ?? codeQuery.data?.detail ?? null;
  const isManaged = codeQuery.data?.managed !== false;
  const isStarting = ensureMutation.isPending || status === 'starting';
  const isReady = !codeQuery.isError && isManaged && status === 'ready';
  const canOpen =
    selectedEnvironmentId !== null && !ensureMutation.isPending && !stopMutation.isPending;
  const canStop =
    !ensureMutation.isPending &&
    !stopMutation.isPending &&
    (status === 'ready' || status === 'starting');

  return (
    <section className="space-y-4 rounded-xl border border-gray-200 bg-gray-50 p-5">
      <div className="space-y-1">
        <h2 className="text-lg font-medium text-gray-900">{t('components.codeServer.title')}</h2>
        <p className="text-sm text-gray-600">
          {t('components.codeServer.descriptionPrefix')}{' '}
          <code className="rounded bg-gray-100 px-1.5 py-0.5">/code/</code>.
        </p>
        <p className="text-sm text-gray-600">
          {t('components.codeServer.selectedEnvironment')}{' '}
          <code className="rounded bg-gray-100 px-1.5 py-0.5">
            {selectedEnvironment
              ? `${selectedEnvironment.alias} · ${selectedEnvironment.display_name}`
              : t('common.notSelected')}
          </code>
        </p>
        <p className="text-sm text-gray-600">
          {t('components.codeServer.workspaceRoot')}{' '}
          <code className="rounded bg-gray-100 px-1.5 py-0.5">{workspaceDir}</code>
        </p>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={() => {
            if (selectedEnvironmentId !== null) {
              ensureMutation.mutate(selectedEnvironmentId);
            }
          }}
          disabled={!canOpen}
          className="rounded-full bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-white transition hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {ensureMutation.isPending
            ? t('components.codeServer.starting')
            : t('components.codeServer.open')}
        </button>
        <button
          type="button"
          onClick={() => stopMutation.mutate()}
          disabled={!canStop}
          className="rounded-full border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 transition hover:border-gray-400 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {stopMutation.isPending
            ? t('components.codeServer.stopping')
            : t('components.codeServer.stop')}
        </button>
      </div>

      {selectedEnvironmentId === null ? (
        <p className="text-sm text-amber-700">
          {t('components.codeServer.selectEnvironmentBeforeOpen')}
        </p>
      ) : null}

      {selectedEnvironment?.auth_kind === 'password' ? (
        <p className="text-sm text-amber-700">{t('components.codeServer.passwordUnsupportedHint')}</p>
      ) : null}

      {isStarting ? <p className="text-sm text-gray-500">{t('components.codeServer.starting')}</p> : null}

      {detail ? (
        <p className="text-sm text-red-700">
          {t('components.codeServer.unavailable')} {detail}
        </p>
      ) : null}

      {!detail && selectedEnvironmentId !== null && !isReady && !isStarting ? (
        <p className="text-sm text-gray-500">{t('components.codeServer.notOpenedYet')}</p>
      ) : null}

      {isReady ? (
        <iframe
          key={`${selectedEnvironmentId ?? 'none'}-${iframeRevision}`}
          title={t('components.codeServer.iframeTitle')}
          src="/code/"
          className="h-[640px] w-full rounded-lg border border-gray-300 bg-white"
        />
      ) : null}
    </section>
  );
}

export default CodeServerCard;
