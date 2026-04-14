import { useQuery } from '@tanstack/react-query';
import { getCodeServerStatus } from '../../api';

function CodeServerCard() {
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
    ? detail ?? 'code-server is not managed for this workspace.'
    : detail ?? 'No status response was returned.';
  const showReady = !codeQuery.isError && isManaged && status === 'ready';

  return (
    <section className="space-y-4 rounded-xl border border-gray-200 bg-gray-50 p-5">
      <div className="space-y-1">
        <h2 className="text-lg font-medium text-gray-900">Workspace browser</h2>
        <p className="text-sm text-gray-600">
          Managed code-server session exposed through the daemon at{' '}
          <code className="rounded bg-gray-100 px-1.5 py-0.5">/code/</code>.
        </p>
        <p className="text-sm text-gray-600">
          Workspace root:{' '}
          <code className="rounded bg-gray-100 px-1.5 py-0.5">{workspaceDir ?? 'unconfigured'}</code>
        </p>
      </div>

      {showStarting ? <p className="text-sm text-gray-500">Starting managed code-server...</p> : null}

      {codeQuery.isError ? (
        <p className="text-sm text-red-700">
          Failed to load workspace browser status
          {requestErrorDetail ? `: ${requestErrorDetail}` : '.'}
        </p>
      ) : null}

      {showUnavailable ? (
        <p className="text-sm text-red-700">Workspace browser unavailable: {unavailableDetail}</p>
      ) : null}

      {showReady ? (
        <iframe
          title="Workspace browser"
          src="/code/"
          className="h-[640px] w-full rounded-lg border border-gray-300 bg-white"
        />
      ) : null}
    </section>
  );
}

export default CodeServerCard;
