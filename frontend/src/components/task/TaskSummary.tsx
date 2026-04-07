import type { TaskReadModel, TaskStatus } from '../../types';

interface Props {
  task: TaskReadModel;
}

const statusColors: Record<TaskStatus, string> = {
  running: 'bg-blue-100 text-blue-700',
  completed: 'bg-green-100 text-green-700',
  failed: 'bg-red-100 text-red-700',
  cancelled: 'bg-gray-100 text-gray-700',
  blocked: 'bg-yellow-100 text-yellow-700',
};

function TaskSummary({ task }: Props) {
  return (
    <div className="p-4 rounded border border-gray-200 bg-gray-50">
      <div className="flex items-center justify-between mb-3">
        <div>
          <span className="text-sm text-gray-500">Task ID: {task.identity.task_id}</span>
        </div>
        <span className={`px-2 py-1 rounded ${statusColors[task.lifecycle.status]}`}>
          {task.lifecycle.status}
        </span>
      </div>
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <span className="text-gray-500">Mode:</span> {task.identity.mode}
        </div>
        <div>
          <span className="text-gray-500">Stage:</span> {task.lifecycle.stage}
        </div>
        <div>
          <span className="text-gray-500">Created:</span> {new Date(task.identity.created_at).toLocaleString()}
        </div>
        <div>
          <span className="text-gray-500">Updated:</span> {new Date(task.identity.updated_at).toLocaleString()}
        </div>
      </div>
      <div className="mt-3 text-sm">
        <span className="text-gray-500">Brief:</span> {task.input_summary.brief}
      </div>
    </div>
  );
}

export default TaskSummary;