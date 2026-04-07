import type { TaskReadModel, TaskStatus } from '../../types';

interface Props {
  task: TaskReadModel;
}

const terminationColors: Partial<Record<TaskStatus, string>> = {
  completed: 'bg-green-100 text-green-700 border-green-200',
  failed: 'bg-red-100 text-red-700 border-red-200',
  cancelled: 'bg-gray-100 text-gray-700 border-gray-200',
  blocked: 'bg-yellow-100 text-yellow-700 border-yellow-200',
};

function TerminationSummary({ task }: Props) {
  const status = task.lifecycle.status;
  const reason = task.result_summary.termination_reason || task.lifecycle.termination_reason;
  const error = task.result_summary.error_summary;
  const resultBrief = task.result_summary.result_brief;
  const colorClass = terminationColors[status] || 'bg-gray-100 text-gray-700 border-gray-200';

  return (
    <div className={`p-4 rounded border ${colorClass}`}>
      <h3 className="font-semibold mb-2">Termination Summary</h3>
      <div className="space-y-2 text-sm">
        <div>
          <span className="font-medium">Status:</span> {status}
        </div>
        <div>
          <span className="font-medium">Reason:</span> {reason || 'Unknown'}
        </div>
        {resultBrief && (
          <div>
            <span className="font-medium">Result:</span> {resultBrief}
          </div>
        )}
        {error && (
          <div className="mt-2 p-2 rounded bg-red-50">
            <span className="font-medium">Error:</span> {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default TerminationSummary;