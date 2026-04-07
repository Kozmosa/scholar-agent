import { useNavigate } from 'react-router-dom';
import { TaskListNavigation } from '../components/common';

function TasksPage() {
  const navigate = useNavigate();

  const handleSelect = (task: { task_id: string }) => {
    navigate(`/tasks/${task.task_id}`);
  };

  return (
    <div className="py-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-[var(--text-h)]">All Tasks</h1>
      </header>
      <TaskListNavigation onSelect={handleSelect} />
    </div>
  );
}

export default TasksPage;