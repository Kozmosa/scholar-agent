import { useQuery } from '@tanstack/react-query';
import { getExecutionContext } from '../../api';

interface Props {
  taskId: string;
}

function ExecutionContext({ taskId }: Props) {
  const contextQuery = useQuery({
    queryKey: ['context', taskId],
    queryFn: getExecutionContext,
  });

  if (contextQuery.isLoading) {
    return <div className="text-gray-500">Loading execution context...</div>;
  }

  if (!contextQuery.data) {
    return <div className="text-gray-500">Unable to fetch execution context</div>;
  }

  const { workspace, session, container, resource_snapshot } = contextQuery.data;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Workspace */}
      <div className="p-3 rounded border border-gray-200">
        <h3 className="text-sm font-semibold mb-2">Workspace</h3>
        <div className="text-sm">
          <div><span className="text-gray-500">Label:</span> {workspace.workspace_label}</div>
          <div><span className="text-gray-500">Project Dir:</span> {workspace.project_dir}</div>
        </div>
      </div>

      {/* Session */}
      <div className="p-3 rounded border border-gray-200">
        <h3 className="text-sm font-semibold mb-2">Session</h3>
        <div className="text-sm">
          <div>
            <span className="text-gray-500">Status:</span>
            <span className={session.connected ? 'text-green-500' : 'text-red-500'}>
              {session.connected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          <div><span className="text-gray-500">Recoverable:</span> {session.recoverable ? 'Yes' : 'No'}</div>
        </div>
      </div>

      {/* Container */}
      <div className="p-3 rounded border border-gray-200">
        <h3 className="text-sm font-semibold mb-2">Container</h3>
        <div className="text-sm">
          <div><span className="text-gray-500">Label:</span> {container.container_label}</div>
          <div>
            <span className="text-gray-500">SSH:</span>
            <span className={container.ssh_available ? 'text-green-500' : 'text-red-500'}>
              {container.ssh_available ? 'Available' : 'Unavailable'}
            </span>
          </div>
        </div>
      </div>

      {/* Resources */}
      <div className="p-3 rounded border border-gray-200">
        <h3 className="text-sm font-semibold mb-2">Resources</h3>
        <div className="text-sm grid grid-cols-2 gap-2">
          {resource_snapshot.gpu !== null && (
            <div><span className="text-gray-500">GPU:</span> {Math.round(resource_snapshot.gpu)}%</div>
          )}
          <div><span className="text-gray-500">CPU:</span> {Math.round(resource_snapshot.cpu)}%</div>
          <div><span className="text-gray-500">Memory:</span> {Math.round(resource_snapshot.memory)}%</div>
          <div><span className="text-gray-500">Disk:</span> {Math.round(resource_snapshot.disk)}%</div>
        </div>
      </div>
    </div>
  );
}

export default ExecutionContext;