import type { Milestone } from '../../types/task';

interface Props {
  milestones: Milestone[];
}

const milestoneColors = {
  completed: 'bg-green-500',
  in_progress: 'bg-blue-500 animate-pulse',
  failed: 'bg-red-500',
  blocked: 'bg-yellow-500',
};

function TaskTimeline({ milestones }: Props) {
  if (!milestones || milestones.length === 0) {
    return <div className="text-gray-500">No milestones recorded</div>;
  }

  return (
    <div className="relative">
      <div className="absolute left-2 top-0 bottom-0 w-0.5 bg-gray-300" />
      <div className="space-y-3">
        {milestones.map((milestone) => (
          <div key={milestone.id} className="relative pl-6">
            <span
              className={`absolute left-0 w-4 h-4 rounded-full ${milestoneColors[milestone.status]}`}
            />
            <div className="flex items-center justify-between">
              <span className="font-medium">{milestone.name}</span>
              <span className="text-sm text-gray-500">
                {new Date(milestone.timestamp).toLocaleString()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TaskTimeline;