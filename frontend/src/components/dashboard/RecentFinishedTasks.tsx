import type { TaskListItem, TaskStatus } from '../../types';
import { Link } from 'react-router-dom';

interface Props {
  tasks: TaskListItem[] | undefined;
  isLoading: boolean;
}

const statusColors: Record<TaskStatus, string> = {
  running: 'bg-blue-100 text-blue-700',
  completed: 'bg-green-100 text-green-700',
  failed: 'bg-red-100 text-red-700',
  cancelled: 'bg-gray-100 text-gray-700',
  blocked: 'bg-yellow-100 text-yellow-700',
};

function RecentFinishedTasks({ tasks, isLoading }: Props) {
  if (isLoading) {
    return <div className="text-gray-500">Loading recent tasks...</div>;
  }

  if (!tasks || tasks.length === 0) {
    return <div className="text-gray-500">No recent finished tasks</div>;
  }

  return (
    <div className="space-y-2">
      {tasks.slice(0, 10).map((task) => (
        <Link
          key={task.task_id}
          to={`/tasks/${task.task_id}`}
          className="block p-3 rounded border border-gray-200 hover:border-[var(--accent)]"
        >
          <div className="flex items-center justify-between">
            <span className="font-medium">{task.title}</span>
            <span className={`px-2 py-1 rounded text-sm ${statusColors[task.status]}`}>
              {task.status}
            </span>
          </div>
          <div className="text-sm text-gray-500 mt-1">
            {task.mode} | {task.termination_reason || 'Completed'}
          </div>
        </Link>
      ))}
    </div>
  );
}

export default RecentFinishedTasks;