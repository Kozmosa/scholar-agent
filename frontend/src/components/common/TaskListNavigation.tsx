import { useQuery } from '@tanstack/react-query';
import { getTasks } from '../../api';
import type { TaskListItem, TaskStatus, TaskMode } from '../../types';
import { useState } from 'react';

interface Props {
  onSelect: (task: TaskListItem) => void;
}

const statusFilters: { value: TaskStatus | 'all'; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'running', label: 'Running' },
  { value: 'completed', label: 'Completed' },
  { value: 'failed', label: 'Failed' },
  { value: 'blocked', label: 'Blocked' },
];

const modeFilters: { value: TaskMode | 'all'; label: string }[] = [
  { value: 'all', label: 'All Modes' },
  { value: 'bounded-discovery', label: 'Discovery' },
  { value: 'bounded-reproduction', label: 'Reproduction' },
];

function TaskListNavigation({ onSelect }: Props) {
  const [statusFilter, setStatusFilter] = useState<TaskStatus | 'all'>('all');
  const [modeFilter, setModeFilter] = useState<TaskMode | 'all'>('all');
  const [sortBy, setSortBy] = useState<'updated' | 'created'>('updated');

  const tasksQuery = useQuery({
    queryKey: ['tasks'],
    queryFn: getTasks,
  });

  if (tasksQuery.isLoading) {
    return <div className="text-gray-500">Loading tasks...</div>;
  }

  if (!tasksQuery.data) {
    return <div className="text-red-500">Failed to load tasks</div>;
  }

  // Filter and sort tasks
  const filteredTasks = tasksQuery.data
    .filter((task) => statusFilter === 'all' || task.status === statusFilter)
    .filter((task) => modeFilter === 'all' || task.mode === modeFilter)
    .sort((a, b) => {
      const aTime = new Date(a.updated_at).getTime();
      const bTime = new Date(b.updated_at).getTime();
      return sortBy === 'updated' ? bTime - aTime : aTime - bTime;
    });

  return (
    <div>
      {/* Filters */}
      <div className="flex flex-wrap gap-4 mb-4">
        <div>
          <label className="text-sm text-gray-500 mr-2">Status:</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as TaskStatus | 'all')}
            className="border rounded px-2 py-1 text-sm"
          >
            {statusFilters.map((f) => (
              <option key={f.value} value={f.value}>
                {f.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="text-sm text-gray-500 mr-2">Mode:</label>
          <select
            value={modeFilter}
            onChange={(e) => setModeFilter(e.target.value as TaskMode | 'all')}
            className="border rounded px-2 py-1 text-sm"
          >
            {modeFilters.map((f) => (
              <option key={f.value} value={f.value}>
                {f.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="text-sm text-gray-500 mr-2">Sort:</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'updated' | 'created')}
            className="border rounded px-2 py-1 text-sm"
          >
            <option value="updated">Recently Updated</option>
            <option value="created">Recently Created</option>
          </select>
        </div>
      </div>

      {/* Task List */}
      <div className="space-y-2">
        {filteredTasks.length === 0 ? (
          <div className="text-gray-500">No tasks match the current filters</div>
        ) : (
          filteredTasks.map((task) => (
            <button
              key={task.task_id}
              onClick={() => onSelect(task)}
              className="w-full p-3 rounded border border-gray-200 hover:border-[var(--accent)] text-left"
            >
              <div className="flex items-center justify-between">
                <span className="font-medium">{task.title}</span>
                <span className="text-sm text-gray-500">{task.status}</span>
              </div>
              <div className="text-sm text-gray-500 mt-1">
                {task.mode} | {task.stage}
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  );
}

export default TaskListNavigation;