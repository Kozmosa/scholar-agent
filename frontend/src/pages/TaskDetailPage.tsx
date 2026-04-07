import { useQuery } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';
import { getTask, getArtifactContent } from '../api';
import type { ArtifactListItem } from '../types';
import TaskSummary from '../components/task/TaskSummary';
import TaskTimeline from '../components/task/TaskTimeline';
import ArtifactPreviewModal from '../components/task/ArtifactPreviewModal';
import ExecutionContext from '../components/task/ExecutionContext';
import TerminationSummary from '../components/task/TerminationSummary';
import { useState } from 'react';

function TaskDetailPage() {
  const { taskId } = useParams<{ taskId: string }>();
  const taskQuery = useQuery({
    queryKey: ['task', taskId],
    queryFn: () => getTask(taskId!),
    enabled: !!taskId,
  });

  const [selectedArtifact, setSelectedArtifact] = useState<ArtifactListItem | null>(null);
  const [showModal, setShowModal] = useState(false);

  const artifactContentQuery = useQuery({
    queryKey: ['artifact', selectedArtifact?.artifact_id, 'content'],
    queryFn: () => getArtifactContent(selectedArtifact!.artifact_id),
    enabled: !!selectedArtifact && showModal,
  });

  const handleArtifactClick = (artifact: ArtifactListItem) => {
    setSelectedArtifact(artifact);
    setShowModal(true);
  };

  if (taskQuery.isLoading) {
    return <div className="p-4 text-gray-500">Loading task details...</div>;
  }

  if (taskQuery.isError || !taskQuery.data) {
    return <div className="p-4 text-red-500">Failed to load task</div>;
  }

  const task = taskQuery.data;

  return (
    <div className="min-h-screen p-4">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-[var(--text-h)]">{task.input_summary.title}</h1>
      </header>

      {/* Task Summary */}
      <section className="mb-6">
        <TaskSummary task={task} />
      </section>

      {/* Timeline / Checkpoints */}
      <section className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Timeline</h2>
        <TaskTimeline milestones={task.progress_summary.milestones} />
      </section>

      {/* Artifacts */}
      <section className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Artifacts</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
          {task.result_summary.recent_artifacts.map((artifact) => (
            <button
              key={artifact.artifact_id}
              onClick={() => handleArtifactClick(artifact)}
              className="p-3 rounded border border-gray-200 hover:border-[var(--accent)] text-left"
            >
              <span className="font-medium">{artifact.display_title}</span>
              <span className="text-sm text-gray-500 ml-2">{artifact.artifact_type}</span>
            </button>
          ))}
        </div>
      </section>

      {/* Execution Context */}
      <section className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Execution Context</h2>
        <ExecutionContext taskId={taskId!} />
      </section>

      {/* Termination Summary */}
      {task.lifecycle.status !== 'running' && (
        <section className="mb-6">
          <TerminationSummary task={task} />
        </section>
      )}

      {/* Artifact Preview Modal */}
      {showModal && selectedArtifact && (
        <ArtifactPreviewModal
          artifact={selectedArtifact}
          content={artifactContentQuery.data}
          isLoading={artifactContentQuery.isLoading}
          onClose={() => setShowModal(false)}
        />
      )}
    </div>
  );
}

export default TaskDetailPage;