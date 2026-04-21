import { useQuery } from '@tanstack/react-query';
import { getCodeServerStatus } from '../../api';
import { useT } from '../../i18n';

interface Props {
  selectedEnvironmentSummary: string | null;
}

function CodeServerCard({ selectedEnvironmentSummary }: Props) {
  const t = useT();
  const codeQuery = useQuery({ queryKey: ['code-server-status'], queryFn: getCodeServerStatus });
  const status = codeQuery.data?.status;
  const detail = codeQuery.data?.detail;
  const workspaceDir = codeQuery.data?.workspace_dir;
  const isManaged = codeQuery.data?.managed === true;
  const requestErrorDetail = codeQuery.error instanceof Error ? codeQuery.error.message : null;

  const showStarting = codeQuery.isLoading || (!codeQuery.isError && isManaged && status === 'starting');
  const showUnavailable =
    !codeQuery.isError && (!isManaged || status === 'unavailable' || status === undefined);
  const unavailableDetail = !isManaged
    ? detail ?? t('components.codeServer.notManaged')
    : detail ?? t('components.codeServer.noStatus');
  const showReady = !codeQuery.isError && isManaged && status === 'ready';

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
            {selectedEnvironmentSummary ?? t('common.notSelected')}
          </code>
        </p>
        <p className="text-sm text-gray-600">
          {t('components.codeServer.workspaceRoot')}{' '}
          <code className="rounded bg-gray-100 px-1.5 py-0.5">{workspaceDir ?? t('common.notConfigured')}</code>
        </p>
      </div>

      {showStarting ? <p className="text-sm text-gray-500">{t('components.codeServer.starting')}</p> : null}

      {codeQuery.isError ? (
        <p className="text-sm text-red-700">
          {t('components.codeServer.loadFailed')}
          {requestErrorDetail ? `: ${requestErrorDetail}` : '.'}
        </p>
      ) : null}

      {showUnavailable ? (
        <p className="text-sm text-red-700">
          {t('components.codeServer.unavailable')} {unavailableDetail}
        </p>
      ) : null}

      {showReady ? (
        <iframe
          title={t('components.codeServer.iframeTitle')}
          src="/code/"
          className="h-[640px] w-full rounded-lg border border-gray-300 bg-white"
        />
      ) : null}
    </section>
  );
}

export default CodeServerCard;
