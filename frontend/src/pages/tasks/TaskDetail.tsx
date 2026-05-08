import { useState } from 'react';
import { Alert } from '../../components/ui';
import { useT } from '../../i18n';
import type { TaskOutputEvent, TaskRecord } from '../../types';
import { statusClassName } from './status';
import MessageStream from './MessageStream';
import TaskInputBar from './TaskInputBar';
import { useTaskMessages } from './useTaskMessages';
import { useTaskActions } from './useTaskActions';

type PanelLayout = 'split' | 'main' | 'aside';

interface Props {
  selectedTask: TaskRecord | null;
  detailError: string | null;
  outputItems: TaskOutputEvent[];
  outputError: string | null;
}

function MetadataRow({
  label,
  value,
  fallback,
}: {
  label: string;
  value: string | number | null;
  fallback: string;
}) {
  return (
    <div className="flex items-start gap-4 border-b border-[var(--border)] py-2 last:border-0">
      <span className="w-28 shrink-0 text-xs text-[var(--text-secondary)]">{label}</span>
      <span
        className="min-w-0 flex-1 truncate text-right text-xs font-medium text-[var(--text)]"
        title={value ? String(value) : fallback}
      >
        {value ?? fallback}
      </span>
    </div>
  );
}

export default function TaskDetail({
  selectedTask,
  detailError,
  outputItems,
  outputError,
}: Props) {
  const t = useT();
  const [layout, setLayout] = useState<PanelLayout>('split');
  const metadataFallback = t('pages.tasks.unavailable');

  const taskId = selectedTask?.task_id ?? null;
  const { messages } = useTaskMessages(taskId, outputItems);
  const actions = useTaskActions(taskId);

  // Determine if input bar should show
  const showInput = selectedTask && (
    selectedTask.status === 'running' ||
    (selectedTask.status === 'succeeded' && selectedTask.execution_engine === 'agent-sdk')
  );

  // Determine pause/resume buttons
  const showPause = selectedTask?.status === 'running' && selectedTask?.execution_engine === 'agent-sdk';
  const showResume = selectedTask?.status === 'paused';

  if (detailError) {
    return (
      <section className="flex min-h-0 flex-1 items-center justify-center rounded-xl border border-[var(--border)] bg-[var(--surface)] p-6">
        <p className="text-sm text-[#ff3b30]">{detailError}</p>
      </section>
    );
  }

  if (!selectedTask) {
    return (
      <section className="flex min-h-0 flex-1 items-center justify-center rounded-xl border border-dashed border-[var(--border)] bg-[var(--surface)] p-6">
        <div className="max-w-sm text-center">
          <h2 className="text-base font-semibold text-[var(--text)]">
            {t('pages.tasks.noTaskSelected')}
          </h2>
          <p className="mt-2 text-sm text-[var(--text-secondary)]">
            {t('pages.tasks.noTaskSelectedDescription')}
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="flex min-h-0 flex-1 flex-col overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--surface)] shadow-sm">
      <header className="border-b border-[var(--border)] px-5 py-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="min-w-0">
            <p className="text-xs font-medium uppercase tracking-wide text-[var(--text-secondary)]">
              {t('pages.tasks.workspaceEyebrow')}
            </p>
            <h1 className="mt-1 truncate text-xl font-semibold tracking-tight text-[var(--text)]">
              {selectedTask.title}
            </h1>
            <p className="mt-1 text-sm text-[var(--text-secondary)]">
              {selectedTask.workspace_summary.label} &middot; {selectedTask.environment_summary.alias} &middot;{' '}
              {selectedTask.environment_summary.display_name}
            </p>
          </div>
          <div className="flex items-center gap-2">
            {showPause && (
              <button
                onClick={() => actions.pause()}
                className="rounded-md bg-[var(--bg-secondary)] px-3 py-1 text-xs font-medium text-[var(--text-secondary)] transition hover:bg-[var(--border)]"
              >
                Pause
              </button>
            )}
            {showResume && (
              <button
                onClick={() => actions.resume()}
                className="rounded-md bg-[var(--bg-secondary)] px-3 py-1 text-xs font-medium text-[var(--text-secondary)] transition hover:bg-[var(--border)]"
              >
                Resume
              </button>
            )}
            <span className={`rounded-full border px-3 py-1 text-xs font-medium ${statusClassName[selectedTask.status]}`}>
              {t(`pages.tasks.status.${selectedTask.status}`)}
            </span>
          </div>
        </div>
        {selectedTask.error_summary ? (
          <Alert variant="error" className="mt-3">
            {selectedTask.error_summary}
          </Alert>
        ) : null}
      </header>

      <div
        className={[
          'grid min-h-0 flex-1 gap-0 overflow-hidden transition-all duration-300 ease-in-out',
          layout === 'split' && 'lg:grid-cols-[minmax(0,1fr)_320px]',
          layout !== 'split' && 'lg:grid-cols-1',
        ]
          .filter(Boolean)
          .join(' ')}
      >
        {layout !== 'aside' && (
          <main className="min-h-0 flex flex-col bg-[var(--surface)]">
            {/* Message stream area */}
            <div className="flex-1 overflow-auto">
              {outputError ? <p className="text-sm text-[#ff3b30] p-4">{outputError}</p> : null}
              <MessageStream messages={messages} />
            </div>

            {/* Input bar */}
            {showInput && (
              <TaskInputBar
                onSubmit={actions.sendPrompt}
                disabled={actions.isPending}
              />
            )}

          </main>
        )}

        {layout !== 'main' && (
          <aside className="min-h-0 overflow-auto border-t border-[var(--border)] bg-[var(--bg)] p-5 lg:border-l lg:border-t-0">
            <div className="mb-2 flex items-center justify-between">
              <h2 className="text-sm font-semibold text-[var(--text)]">
                {t('pages.tasks.summary')}
              </h2>
              <button
                type="button"
                onClick={() => setLayout(layout === 'aside' ? 'split' : 'aside')}
                className="rounded-md bg-[var(--bg-secondary)] px-2 py-1 text-xs font-medium text-[var(--text-secondary)] transition hover:bg-[var(--border)]"
                aria-label={
                  layout === 'aside'
                    ? t('pages.tasks.collapseSummary')
                    : t('pages.tasks.expandSummary')
                }
              >
                {layout === 'aside' ? '>>' : '<<'}
              </button>
            </div>
            <div className="space-y-5">
              <section>
                <div className="rounded-xl border border-[var(--border)] bg-[var(--surface)] px-3">
                  <MetadataRow label={t('pages.tasks.taskId')} value={selectedTask.task_id} fallback={metadataFallback} />
                  <MetadataRow label={t('pages.tasks.created')} value={selectedTask.created_at} fallback={metadataFallback} />
                  <MetadataRow label={t('pages.tasks.updated')} value={selectedTask.updated_at} fallback={metadataFallback} />
                  <MetadataRow label={t('pages.tasks.started')} value={selectedTask.started_at} fallback={metadataFallback} />
                  <MetadataRow label={t('pages.tasks.completed')} value={selectedTask.completed_at} fallback={metadataFallback} />
                </div>
              </section>

              <section>
                <h2 className="mb-2 text-sm font-semibold text-[var(--text)]">
                  {t('pages.tasks.binding')}
                </h2>
                {selectedTask.binding ? (
                  <div className="rounded-xl border border-[var(--border)] bg-[var(--surface)] px-3">
                    <MetadataRow label={t('pages.tasks.profile')} value={selectedTask.binding.task_profile} fallback={metadataFallback} />
                    <MetadataRow label={t('pages.tasks.workdir')} value={selectedTask.binding.resolved_workdir} fallback={metadataFallback} />
                    <MetadataRow label={t('pages.tasks.snapshot')} value={selectedTask.binding.snapshot_path} fallback={metadataFallback} />
                  </div>
                ) : (
                  <p className="text-sm text-[var(--text-secondary)]">
                    {t('pages.tasks.bindingUnavailable')}
                  </p>
                )}
              </section>

              <section>
                <h2 className="mb-2 text-sm font-semibold text-[var(--text)]">
                  {t('pages.tasks.runtime')}
                </h2>
                {selectedTask.runtime ? (
                  <div className="rounded-xl border border-[var(--border)] bg-[var(--surface)] px-3">
                    <MetadataRow label={t('pages.tasks.runner')} value={selectedTask.runtime.runner_kind} fallback={metadataFallback} />
                    <MetadataRow label={t('pages.tasks.directory')} value={selectedTask.runtime.working_directory} fallback={metadataFallback} />
                    <MetadataRow
                      label={t('pages.tasks.command')}
                      value={selectedTask.runtime.command.join(' ') || t('pages.tasks.pendingValue')}
                      fallback={metadataFallback}
                    />
                  </div>
                ) : (
                  <p className="text-sm text-[var(--text-secondary)]">
                    {t('pages.tasks.runtimeUnavailable')}
                  </p>
                )}
              </section>

              <section>
                <h2 className="mb-2 text-sm font-semibold text-[var(--text)]">
                  {t('pages.tasks.result')}
                </h2>
                <div className="rounded-xl border border-[var(--border)] bg-[var(--surface)] px-3">
                  <MetadataRow label={t('pages.tasks.exitCode')} value={selectedTask.result.exit_code} fallback={metadataFallback} />
                  <MetadataRow label={t('pages.tasks.failure')} value={selectedTask.result.failure_category} fallback={metadataFallback} />
                  <MetadataRow label={t('pages.tasks.completed')} value={selectedTask.result.completed_at} fallback={metadataFallback} />
                </div>
              </section>

              <section>
                <h2 className="mb-2 text-sm font-semibold text-[var(--text)]">
                  {t('pages.tasks.prompt')}
                </h2>
                {selectedTask.prompt ? (
                  <div className="space-y-2">
                    {selectedTask.prompt.layers.map((layer) => (
                      <details
                        key={layer.name}
                        className="rounded-lg border border-[var(--border)] bg-[var(--surface)]"
                      >
                        <summary className="cursor-pointer px-3 py-2 text-xs font-medium text-[var(--text)]">
                          {layer.label}{' '}
                          <span className="text-[var(--text-secondary)]">
                            ({layer.char_count} {t('pages.tasks.chars')})
                          </span>
                        </summary>
                        <pre className="max-h-48 overflow-auto border-t border-[var(--border)] bg-[var(--bg-tertiary)] p-3 text-xs text-[var(--text)]">
                          {layer.content}
                        </pre>
                      </details>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-[var(--text-secondary)]">
                    {t('pages.tasks.promptUnavailable')}
                  </p>
                )}
              </section>
            </div>
          </aside>
        )}
      </div>
    </section>
  );
}
