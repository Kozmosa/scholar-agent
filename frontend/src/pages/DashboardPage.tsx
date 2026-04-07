import { useQuery } from '@tanstack/react-query';
import { getHealth, getRunningTasks, getRecentTasks, getRecentArtifacts, getResourceSnapshot } from '../api';
import HealthStatusBar from '../components/dashboard/HealthStatusBar';
import RunningTaskTimeline from '../components/dashboard/RunningTaskTimeline';
import RecentFinishedTasks from '../components/dashboard/RecentFinishedTasks';
import RecentArtifacts from '../components/dashboard/RecentArtifacts';
import ResourceSnapshot from '../components/dashboard/ResourceSnapshot';

function DashboardPage() {
  const healthQuery = useQuery({ queryKey: ['health'], queryFn: getHealth });
  const runningTasksQuery = useQuery({ queryKey: ['tasks', 'running'], queryFn: getRunningTasks });
  const recentTasksQuery = useQuery({ queryKey: ['tasks', 'recent'], queryFn: getRecentTasks });
  const recentArtifactsQuery = useQuery({ queryKey: ['artifacts', 'recent'], queryFn: getRecentArtifacts });
  const resourcesQuery = useQuery({ queryKey: ['resources'], queryFn: getResourceSnapshot });

  return (
    <div className="min-h-screen p-4">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-[var(--text-h)]">Research Dashboard</h1>
      </header>

      {/* System Health Status Bar */}
      <HealthStatusBar health={healthQuery.data} isLoading={healthQuery.isLoading} />

      {/* Running Task Timeline */}
      <section className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Running Tasks</h2>
        <RunningTaskTimeline tasks={runningTasksQuery.data} isLoading={runningTasksQuery.isLoading} />
      </section>

      {/* Recent Finished Tasks */}
      <section className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Recent Finished Tasks</h2>
        <RecentFinishedTasks tasks={recentTasksQuery.data} isLoading={recentTasksQuery.isLoading} />
      </section>

      {/* Recent Artifacts */}
      <section className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Recent Artifacts</h2>
        <RecentArtifacts artifacts={recentArtifactsQuery.data} isLoading={recentArtifactsQuery.isLoading} />
      </section>

      {/* Resource Snapshot */}
      <section className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Resources</h2>
        <ResourceSnapshot snapshot={resourcesQuery.data} isLoading={resourcesQuery.isLoading} />
      </section>
    </div>
  );
}

export default DashboardPage;