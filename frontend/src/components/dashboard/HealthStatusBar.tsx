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

  const statusColor = health.api_status === 'ok' ? 'green' : health.api_status === 'degraded' ? 'yellow' : 'red';

  return (
    <div className="flex items-center gap-4 p-2 rounded bg-gray-50 border border-gray-200">
      <div className="flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${statusColor === 'green' ? 'bg-green-500' : statusColor === 'yellow' ? 'bg-yellow-500' : 'bg-red-500'}`} />
        <span className="text-sm">API: {health.api_status}</span>
      </div>
      <div className="flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${health.ssh_available ? 'bg-green-500' : 'bg-red-500'}`} />
        <span className="text-sm">SSH: {health.ssh_available ? 'Available' : 'Unavailable'}</span>
      </div>
      <div className="flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${health.workspace_ready ? 'bg-green-500' : 'bg-yellow-500'}`} />
        <span className="text-sm">Workspace: {health.workspace_ready ? 'Ready' : 'Not Ready'}</span>
      </div>
    </div>
  );
}

export default HealthStatusBar;