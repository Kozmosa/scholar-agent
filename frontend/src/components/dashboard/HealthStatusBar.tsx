import type { SystemHealth } from '../../types';

interface Props {
  health: SystemHealth | undefined;
  isLoading: boolean;
}

function HealthStatusBar({ health, isLoading }: Props) {
  if (isLoading) {
    return (
      <div className="p-2 rounded bg-gray-100 text-gray-500">
        Loading system status...
      </div>
    );
  }

  if (!health) {
    return (
      <div className="p-2 rounded bg-red-100 text-red-700">
        Unable to fetch system status
      </div>
    );
  }

  const statusColor = health.status === 'ok' ? 'green' : 'yellow';
  const sshOk = health.container_health?.ssh_ok ?? false;
  const workspaceReady = health.container_health?.project_dir_writable ?? false;

  return (
    <div className="flex flex-wrap items-center gap-4 p-2 rounded bg-gray-50 border border-gray-200">
      <div className="flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${statusColor === 'green' ? 'bg-green-500' : 'bg-yellow-500'}`} />
        <span className="text-sm">API: {health.status}</span>
      </div>
      <div className="flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${health.container_configured ? 'bg-green-500' : 'bg-gray-400'}`} />
        <span className="text-sm">Container: {health.container_configured ? 'Configured' : 'Not configured'}</span>
      </div>
      <div className="flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${sshOk ? 'bg-green-500' : 'bg-red-500'}`} />
        <span className="text-sm">SSH: {sshOk ? 'Available' : 'Unavailable'}</span>
      </div>
      <div className="flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${workspaceReady ? 'bg-green-500' : 'bg-yellow-500'}`} />
        <span className="text-sm">Workspace: {workspaceReady ? 'Writable' : 'Not ready'}</span>
      </div>
    </div>
  );
}

export default HealthStatusBar;