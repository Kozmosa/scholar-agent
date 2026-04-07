import type { TaskListItem } from '../../types';
import { Link } from 'react-router-dom';

interface Props {
  tasks: TaskListItem[] | undefined;
  isLoading: boolean;
}

function RunningTaskTimeline({ tasks, isLoading }: Props) {
  if (isLoading) {
    return <div className="text-gray-500">Loading running tasks...</div>;
  }

  if (!tasks || tasks.length === 0) {
    return <div className="text-gray-500">No running tasks</div>;
  }

  return (
    <div className="space-y-2">
      {tasks.map((task) => (
        <Link
          key={task.task_id}
          to={`/tasks/${task.task_id}`}
          className="block p-3 rounded border border-gray-200 hover:border-[var(--accent)] hover:bg-[var(--accent-bg)]"
        >
          <div className="flex items-center justify-between">
            <div>
              <span className="font-medium">{task.title}</span>
              <span className="ml-2 text-sm text-gray-500">{task.mode}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm">{task.stage}</span>
              <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
            </div>
          </div>
          <div className="text-sm text-gray-500 mt-1">
            Updated: {new Date(task.updated_at).toLocaleString()}
          </div>
        </Link>
      ))}
    </div>
  );
}

export default RunningTaskTimeline;