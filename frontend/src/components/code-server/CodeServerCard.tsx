import { useQuery } from '@tanstack/react-query';
import { getCodeServerStatus } from '../../api';

function CodeServerCard() {
  const codeQuery = useQuery({ queryKey: ['code-server-status'], queryFn: getCodeServerStatus });
  const status = codeQuery.data?.status ?? 'starting';
  const detail = codeQuery.data?.detail;
  const workspaceDir = codeQuery.data?.workspace_dir;

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

      {codeQuery.isLoading || status === 'starting' ? (
        <p className="text-sm text-gray-500">Starting managed code-server...</p>
      ) : null}

      {status === 'unavailable' ? (
        <p className="text-sm text-red-700">Workspace browser unavailable{detail ? `: ${detail}` : '.'}</p>
      ) : null}

      {status === 'ready' ? (
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
