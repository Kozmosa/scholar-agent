import { useQuery } from '@tanstack/react-query';
import { getHealth } from '../api';
import { HealthStatusBar, TerminalBenchCard } from '../components';

function DashboardPage() {
  const healthQuery = useQuery({ queryKey: ['health'], queryFn: getHealth });

  return (
    <div className="py-8 px-4 sm:px-6 lg:px-8">
      <section className="mb-8 space-y-3">
        <p className="text-sm font-medium uppercase tracking-wide text-[var(--accent)]">
          Service status
        </p>
        <h1 className="text-3xl font-semibold text-gray-900">Scholar Agent terminal shell</h1>
        <p className="max-w-3xl text-sm text-gray-600 sm:text-base">
          The frontend now exposes the cleaned runtime shell: health checks plus the single-session
          terminal bench control surface. Use this page to confirm API, SSH, workspace readiness,
          and terminal session state.
        </p>
      </section>

      <section className="space-y-4 rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <div className="space-y-1">
          <h2 className="text-lg font-medium text-gray-900">Current backend surface</h2>
          <p className="text-sm text-gray-600">
            Available endpoints: <code className="rounded bg-gray-100 px-1.5 py-0.5">/health</code>,{' '}
            <code className="rounded bg-gray-100 px-1.5 py-0.5">/v1/health</code>,{' '}
            <code className="rounded bg-gray-100 px-1.5 py-0.5">/terminal/session</code>, and{' '}
            <code className="rounded bg-gray-100 px-1.5 py-0.5">/v1/terminal/session</code>.
          </p>
          <p className="text-sm text-gray-600">
            State root:{' '}
            <code className="rounded bg-gray-100 px-1.5 py-0.5">
              {healthQuery.data?.state_root ?? '.ainrf'}
            </code>
          </p>
          {healthQuery.data?.detail ? (
            <p className="text-sm text-yellow-700">Detail: {healthQuery.data.detail}</p>
          ) : null}
        </div>
        <HealthStatusBar health={healthQuery.data} isLoading={healthQuery.isLoading} />
        <TerminalBenchCard />
      </section>
    </div>
  );
}

export default DashboardPage;
