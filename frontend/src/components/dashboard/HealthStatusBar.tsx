import type { SystemHealth } from '../../types';
import { useT } from '../../i18n';

interface Props {
  health: SystemHealth | undefined;
  isLoading: boolean;
}

function HealthStatusBar({ health, isLoading }: Props) {
  const t = useT();

  if (isLoading) {
    return (
      <div className="rounded bg-gray-100 p-2 text-gray-500">
        {t('components.healthStatusBar.loading')}
      </div>
    );
  }

  if (!health) {
    return (
      <div className="rounded bg-red-100 p-2 text-red-700">
        {t('components.healthStatusBar.unable')}
      </div>
    );
  }

  const statusColor = health.status === 'ok' ? 'green' : 'yellow';
  const sshOk = health.container_health?.ssh_ok ?? false;
  const workspaceReady = health.container_health?.project_dir_writable ?? false;
  const containerConfigured = health.container_configured ? t('common.configured') : t('common.notConfigured');
  const apiStatus = health.status === 'ok' ? t('common.ok') : t('common.degraded');

  return (
    <div className="flex flex-wrap items-center gap-4 rounded border border-gray-200 bg-gray-50 p-2">
      <div className="flex items-center gap-2">
        <span
          className={`h-2 w-2 rounded-full ${statusColor === 'green' ? 'bg-green-500' : 'bg-yellow-500'}`}
        />
        <span className="text-sm">
          {t('components.healthStatusBar.apiLabel')} {apiStatus}
        </span>
      </div>
      <div className="flex items-center gap-2">
        <span
          className={`h-2 w-2 rounded-full ${health.container_configured ? 'bg-green-500' : 'bg-gray-400'}`}
        />
        <span className="text-sm">
          {t('components.healthStatusBar.containerLabel')} {containerConfigured}
        </span>
      </div>
      <div className="flex items-center gap-2">
        <span className={`h-2 w-2 rounded-full ${sshOk ? 'bg-green-500' : 'bg-red-500'}`} />
        <span className="text-sm">
          {t('components.healthStatusBar.sshLabel')} {sshOk ? t('common.available') : t('common.unavailable')}
        </span>
      </div>
      <div className="flex items-center gap-2">
        <span
          className={`h-2 w-2 rounded-full ${workspaceReady ? 'bg-green-500' : 'bg-yellow-500'}`}
        />
        <span className="text-sm">
          {t('components.healthStatusBar.workspaceLabel')} {workspaceReady ? t('common.writable') : t('common.notReady')}
        </span>
      </div>
    </div>
  );
}

export default HealthStatusBar;
