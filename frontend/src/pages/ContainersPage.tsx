import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useMemo, useState, type FormEvent } from 'react';
import {
  createEnvironment,
  deleteEnvironment,
  detectEnvironment,
  getEnvironments,
  updateEnvironment,
} from '../api';
import type {
  EnvironmentAuthKind,
  EnvironmentCreateRequest,
  EnvironmentListResponse,
  EnvironmentRecord,
  EnvironmentUpdateRequest,
} from '../types';

const environmentsQueryKey = ['environments'] as const;
const EMPTY_ENVIRONMENTS: EnvironmentRecord[] = [];

type EnvironmentEditorMode = 'create' | 'edit';

interface EnvironmentFormValues {
  alias: string;
  display_name: string;
  description: string;
  tags: string;
  host: string;
  port: string;
  user: string;
  auth_kind: EnvironmentAuthKind;
  identity_file: string;
  proxy_jump: string;
  proxy_command: string;
  ssh_options: string;
  default_workdir: string;
  preferred_python: string;
  preferred_env_manager: string;
  preferred_runtime_notes: string;
}

const emptyFormValues = (): EnvironmentFormValues => ({
  alias: '',
  display_name: '',
  description: '',
  tags: '',
  host: '',
  port: '22',
  user: 'root',
  auth_kind: 'ssh_key',
  identity_file: '',
  proxy_jump: '',
  proxy_command: '',
  ssh_options: '{}',
  default_workdir: '',
  preferred_python: '',
  preferred_env_manager: '',
  preferred_runtime_notes: '',
});

function valuesFromEnvironment(environment: EnvironmentRecord): EnvironmentFormValues {
  return {
    alias: environment.alias,
    display_name: environment.display_name,
    description: environment.description ?? '',
    tags: environment.tags.join(', '),
    host: environment.host,
    port: String(environment.port),
    user: environment.user,
    auth_kind: environment.auth_kind,
    identity_file: environment.identity_file ?? '',
    proxy_jump: environment.proxy_jump ?? '',
    proxy_command: environment.proxy_command ?? '',
    ssh_options: JSON.stringify(environment.ssh_options, null, 2),
    default_workdir: environment.default_workdir ?? '',
    preferred_python: environment.preferred_python ?? '',
    preferred_env_manager: environment.preferred_env_manager ?? '',
    preferred_runtime_notes: environment.preferred_runtime_notes ?? '',
  };
}

function parseTags(value: string): string[] {
  return value
    .split(',')
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

function parseJsonObject(value: string): Record<string, string> {
  const trimmed = value.trim();
  if (!trimmed) {
    return {};
  }

  const parsed: unknown = JSON.parse(trimmed) as unknown;
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new Error('SSH options must be a JSON object');
  }

  const entries = Object.entries(parsed as Record<string, unknown>);
  const normalized: Record<string, string> = {};
  for (const [key, entryValue] of entries) {
    if (typeof entryValue !== 'string') {
      throw new Error('SSH options values must be strings');
    }
    normalized[key] = entryValue;
  }
  return normalized;
}

function formatTimestamp(value: string | null): string {
  if (!value) {
    return 'never';
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return parsed.toLocaleString();
}

function mergeEnvironmentList(
  current: EnvironmentListResponse | undefined,
  environment: EnvironmentRecord
): EnvironmentListResponse {
  const items = current?.items ?? [];
  const nextItems = [...items];
  const index = nextItems.findIndex((item) => item.id === environment.id);
  if (index === -1) {
    nextItems.unshift(environment);
  } else {
    nextItems[index] = environment;
  }
  return { items: nextItems };
}

function removeEnvironmentFromList(
  current: EnvironmentListResponse | undefined,
  environmentId: string
): EnvironmentListResponse {
  return {
    items: (current?.items ?? []).filter((item) => item.id !== environmentId),
  };
}

interface EnvironmentEditorProps {
  mode: EnvironmentEditorMode;
  environment: EnvironmentRecord | null;
  activeEnvironment: EnvironmentRecord | null;
  isSaving: boolean;
  onSubmit: (values: EnvironmentFormValues) => Promise<void>;
  onCancel: () => void;
}

function EnvironmentEditor({
  mode,
  environment,
  activeEnvironment,
  isSaving,
  onSubmit,
  onCancel,
}: EnvironmentEditorProps) {
  const [values, setValues] = useState<EnvironmentFormValues>(() =>
    environment ? valuesFromEnvironment(environment) : emptyFormValues()
  );
  const [formError, setFormError] = useState<string | null>(null);

  const title = mode === 'create' ? 'Create environment' : 'Edit environment';
  const submitLabel = mode === 'create' ? 'Create environment' : 'Save changes';

  const updateField = (field: keyof EnvironmentFormValues, nextValue: string) => {
    setValues((current) => ({ ...current, [field]: nextValue }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      setFormError(null);
      await onSubmit(values);
    } catch (error) {
      setFormError(error instanceof Error ? error.message : 'Unable to save environment');
    }
  };

  return (
    <section className="space-y-5 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="space-y-2">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--accent)]">
          Environment editor
        </p>
        <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
        <p className="text-sm text-gray-600">
          Define SSH target details, runtime preferences, and the minimal metadata that powers the
          Containers control plane.
        </p>
      </div>

      {activeEnvironment ? (
        <div
          data-testid="active-environment-banner"
          className="rounded-2xl border border-gray-200 bg-gray-50 p-4 text-sm text-gray-700"
        >
          Active environment: <span className="font-medium text-gray-900">{activeEnvironment.alias}</span>
          <span className="ml-2 text-gray-500">({activeEnvironment.display_name})</span>
        </div>
      ) : (
        <div className="rounded-2xl border border-dashed border-gray-300 bg-gray-50 p-4 text-sm text-gray-500">
          No environment has been marked as active yet.
        </div>
      )}

      <form className="space-y-5" onSubmit={handleSubmit}>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Alias</span>
            <input
              required
              value={values.alias}
              onChange={(event) => updateField('alias', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
              placeholder="gpu-lab"
            />
          </label>

          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Display name</span>
            <input
              required
              value={values.display_name}
              onChange={(event) => updateField('display_name', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
              placeholder="GPU Lab"
            />
          </label>
        </div>

        <label className="space-y-2">
          <span className="text-sm font-medium text-gray-900">Description</span>
          <textarea
            value={values.description}
            onChange={(event) => updateField('description', event.target.value)}
            rows={3}
            className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
            placeholder="Primary training environment"
          />
        </label>

        <div className="grid gap-4 sm:grid-cols-2">
          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Host</span>
            <input
              required
              value={values.host}
              onChange={(event) => updateField('host', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
              placeholder="gpu.example.com"
            />
          </label>

          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Port</span>
            <input
              required
              type="number"
              min={1}
              max={65535}
              value={values.port}
              onChange={(event) => updateField('port', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
            />
          </label>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">User</span>
            <input
              value={values.user}
              onChange={(event) => updateField('user', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
              placeholder="root"
            />
          </label>

          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Auth kind</span>
            <select
              value={values.auth_kind}
              onChange={(event) => updateField('auth_kind', event.target.value as EnvironmentAuthKind)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
            >
              <option value="ssh_key">SSH key</option>
              <option value="password">Password</option>
              <option value="agent">Agent</option>
            </select>
          </label>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Identity file</span>
            <input
              value={values.identity_file}
              onChange={(event) => updateField('identity_file', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
              placeholder="/keys/gpu-lab"
            />
          </label>

          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Proxy jump</span>
            <input
              value={values.proxy_jump}
              onChange={(event) => updateField('proxy_jump', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
              placeholder="bastion"
            />
          </label>
        </div>

        <label className="space-y-2">
          <span className="text-sm font-medium text-gray-900">Proxy command</span>
          <input
            value={values.proxy_command}
            onChange={(event) => updateField('proxy_command', event.target.value)}
            className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
            placeholder="ssh -W %h:%p bastion"
          />
        </label>

        <div className="grid gap-4 sm:grid-cols-2">
          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Tags</span>
            <input
              value={values.tags}
              onChange={(event) => updateField('tags', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
              placeholder="gpu, research"
            />
          </label>

          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Default workdir</span>
            <input
              value={values.default_workdir}
              onChange={(event) => updateField('default_workdir', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
              placeholder="/workspace/project"
            />
          </label>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Preferred Python</span>
            <input
              value={values.preferred_python}
              onChange={(event) => updateField('preferred_python', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
              placeholder="python3.13"
            />
          </label>

          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-900">Preferred env manager</span>
            <input
              value={values.preferred_env_manager}
              onChange={(event) => updateField('preferred_env_manager', event.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
              placeholder="uv"
            />
          </label>
        </div>

        <label className="space-y-2">
          <span className="text-sm font-medium text-gray-900">Preferred runtime notes</span>
          <textarea
            value={values.preferred_runtime_notes}
            onChange={(event) => updateField('preferred_runtime_notes', event.target.value)}
            rows={3}
            className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)]"
            placeholder="Use CUDA 12 image"
          />
        </label>

        <label className="space-y-2">
          <span className="text-sm font-medium text-gray-900">SSH options JSON</span>
          <textarea
            value={values.ssh_options}
            onChange={(event) => updateField('ssh_options', event.target.value)}
            rows={4}
            className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 font-mono text-sm outline-none transition focus:border-[var(--accent)]"
            placeholder='{"StrictHostKeyChecking":"no"}'
          />
        </label>

        {formError ? (
          <p className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {formError}
          </p>
        ) : null}

        <div className="flex flex-wrap items-center gap-3">
          <button
            type="submit"
            disabled={isSaving}
            className="rounded-full bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-white transition hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {isSaving ? 'Saving…' : submitLabel}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="rounded-full border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 transition hover:border-gray-400 hover:bg-gray-50"
          >
            {mode === 'create' ? 'Reset' : 'Cancel edit'}
          </button>
        </div>
      </form>
    </section>
  );
}

function ContainersPage() {
  const queryClient = useQueryClient();
  const environmentsQuery = useQuery({
    queryKey: environmentsQueryKey,
    queryFn: getEnvironments,
  });
  const [editorMode, setEditorMode] = useState<EnvironmentEditorMode>('create');
  const [editorEnvironmentId, setEditorEnvironmentId] = useState<string | null>(null);
  const [activeEnvironmentId, setActiveEnvironmentId] = useState<string | null>(null);
  const [editorFormKey, setEditorFormKey] = useState(0);

  const environments = environmentsQuery.data?.items ?? EMPTY_ENVIRONMENTS;
  const editorEnvironment = useMemo(
    () => environments.find((environment) => environment.id === editorEnvironmentId) ?? null,
    [environments, editorEnvironmentId]
  );
  const activeEnvironment = useMemo(
    () => environments.find((environment) => environment.id === activeEnvironmentId) ?? null,
    [environments, activeEnvironmentId]
  );

  const syncEnvironmentList = (next: EnvironmentListResponse) => {
    queryClient.setQueryData(environmentsQueryKey, next);
  };

  const saveMutation = useMutation({
    mutationFn: async (values: EnvironmentFormValues) => {
      const requestBase = {
        alias: values.alias.trim(),
        display_name: values.display_name.trim(),
        description: values.description.trim() || null,
        tags: parseTags(values.tags),
        host: values.host.trim(),
        port: Number.parseInt(values.port, 10),
        user: values.user.trim() || 'root',
        auth_kind: values.auth_kind,
        identity_file: values.identity_file.trim() || null,
        proxy_jump: values.proxy_jump.trim() || null,
        proxy_command: values.proxy_command.trim() || null,
        ssh_options: parseJsonObject(values.ssh_options),
        default_workdir: values.default_workdir.trim() || null,
        preferred_python: values.preferred_python.trim() || null,
        preferred_env_manager: values.preferred_env_manager.trim() || null,
        preferred_runtime_notes: values.preferred_runtime_notes.trim() || null,
      } satisfies EnvironmentCreateRequest;

      if (!Number.isInteger(requestBase.port) || requestBase.port < 1 || requestBase.port > 65535) {
        throw new Error('Port must be between 1 and 65535');
      }

      if (editorMode === 'create') {
        return createEnvironment(requestBase);
      }

      if (editorEnvironmentId === null) {
        throw new Error('No environment is selected for editing');
      }

      const request: EnvironmentUpdateRequest = requestBase;
      return updateEnvironment(editorEnvironmentId, request);
    },
    onSuccess: (environment) => {
      const current = queryClient.getQueryData<EnvironmentListResponse>(environmentsQueryKey);
      syncEnvironmentList(mergeEnvironmentList(current, environment));
      setActiveEnvironmentId(environment.id);
      setEditorEnvironmentId(environment.id);
      setEditorMode('edit');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (environmentId: string) => deleteEnvironment(environmentId),
    onSuccess: (_, environmentId) => {
      const current = queryClient.getQueryData<EnvironmentListResponse>(environmentsQueryKey);
      syncEnvironmentList(removeEnvironmentFromList(current, environmentId));
      if (activeEnvironmentId === environmentId) {
        setActiveEnvironmentId(null);
      }
      if (editorEnvironmentId === environmentId) {
        setEditorEnvironmentId(null);
        setEditorMode('create');
      }
    },
  });

  const detectMutation = useMutation({
    mutationFn: async (environmentId: string) => detectEnvironment(environmentId),
    onSuccess: (environment) => {
      const current = queryClient.getQueryData<EnvironmentListResponse>(environmentsQueryKey);
      syncEnvironmentList(mergeEnvironmentList(current, environment));
    },
  });

  const requestError = environmentsQuery.error instanceof Error ? environmentsQuery.error.message : null;
  const activeEnvironmentSummary = activeEnvironment
    ? `${activeEnvironment.alias} · ${activeEnvironment.display_name}`
    : 'No active environment selected yet';

  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <section className="mb-8 space-y-3">
        <p className="text-sm font-medium uppercase tracking-wide text-[var(--accent)]">Containers</p>
        <h1 className="text-3xl font-semibold text-gray-900">Environment control plane</h1>
        <p className="max-w-3xl text-sm text-gray-600 sm:text-base">
          Manage SSH-backed runtime environments, trigger manual detection, and keep a single
          active environment ready for the terminal and workspace surfaces.
        </p>
      </section>

      <section className="mb-6 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-sm font-medium uppercase tracking-wide text-[var(--accent)]">Current selection</p>
            <p className="mt-1 text-sm text-gray-600">{activeEnvironmentSummary}</p>
          </div>
          <button
            type="button"
            onClick={() => {
              setEditorFormKey((value) => value + 1);
              setEditorMode('create');
              setEditorEnvironmentId(null);
            }}
            className="rounded-full bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-white transition hover:opacity-95"
          >
            Add environment
          </button>
        </div>
      </section>

      <div className="grid gap-6 xl:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)]">
        <section className="space-y-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <div className="space-y-1">
            <h2 className="text-xl font-semibold text-gray-900">Environment list</h2>
            <p className="text-sm text-gray-600">
              Use the list to inspect the current control-plane state, run detection, or mark an
              environment active for downstream pages.
            </p>
          </div>

          {environmentsQuery.isLoading ? (
            <p className="text-sm text-gray-500">Loading environments...</p>
          ) : null}

          {requestError ? <p className="text-sm text-red-700">{requestError}</p> : null}

          {!environmentsQuery.isLoading && environments.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-gray-300 bg-gray-50 p-6 text-sm text-gray-500">
              No environments have been created yet.
            </div>
          ) : null}

          {environments.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 text-left text-sm">
                <thead className="bg-gray-50 text-gray-600">
                  <tr>
                    <th className="px-4 py-3 font-medium">Alias</th>
                    <th className="px-4 py-3 font-medium">Host</th>
                    <th className="px-4 py-3 font-medium">Auth</th>
                    <th className="px-4 py-3 font-medium">Detection</th>
                    <th className="px-4 py-3 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {environments.map((environment) => {
                    const detection = environment.latest_detection;
                    const isActive = environment.id === activeEnvironmentId;
                    const isEditing = environment.id === editorEnvironmentId;
                    return (
                      <tr
                        key={environment.id}
                        className={isActive ? 'bg-[var(--accent)]/5' : 'bg-white'}
                      >
                        <td className="px-4 py-4">
                          <div className="space-y-1">
                            <p className="font-medium text-gray-900">
                              {environment.display_name}
                              {isActive ? (
                                <span className="ml-2 rounded-full bg-[var(--accent)]/10 px-2 py-0.5 text-xs font-semibold text-[var(--accent)]">
                                  Active
                                </span>
                              ) : null}
                            </p>
                            <p className="text-xs text-gray-500">
                              <code className="rounded bg-gray-100 px-1.5 py-0.5">{environment.alias}</code>
                              {isEditing ? (
                                <span className="ml-2 text-[var(--accent)]">Editing</span>
                              ) : null}
                            </p>
                            <p className="text-xs text-gray-500">{environment.default_workdir ?? 'No default workdir'}</p>
                          </div>
                        </td>
                        <td className="px-4 py-4 text-gray-700">
                          <div>{environment.host}</div>
                          <div className="text-xs text-gray-500">
                            {environment.user}@{environment.port}
                          </div>
                        </td>
                        <td className="px-4 py-4 text-gray-700">
                          <div className="capitalize">{environment.auth_kind.replace('_', ' ')}</div>
                          <div className="text-xs text-gray-500">
                            {environment.tags.length > 0 ? environment.tags.join(', ') : 'No tags'}
                          </div>
                        </td>
                        <td className="px-4 py-4">
                          {detection ? (
                            <div className="space-y-1">
                              <div className="text-sm font-medium text-gray-900">
                                {detection.status} · {detection.summary}
                              </div>
                              <div className="text-xs text-gray-500">
                                Detected {formatTimestamp(detection.detected_at)}
                              </div>
                            </div>
                          ) : (
                            <span className="text-sm text-gray-500">Not detected yet</span>
                          )}
                        </td>
                        <td className="px-4 py-4">
                          <div className="flex flex-wrap gap-2">
                            <button
                              type="button"
                              onClick={() => setActiveEnvironmentId(environment.id)}
                              className="rounded-full border border-gray-300 bg-white px-3 py-1.5 text-xs font-semibold text-gray-700 transition hover:border-gray-400 hover:bg-gray-50"
                            >
                              Use
                            </button>
                            <button
                              type="button"
                              onClick={() => {
                                setEditorMode('edit');
                                setEditorEnvironmentId(environment.id);
                              }}
                              className="rounded-full border border-gray-300 bg-white px-3 py-1.5 text-xs font-semibold text-gray-700 transition hover:border-gray-400 hover:bg-gray-50"
                            >
                              Edit
                            </button>
                            <button
                              type="button"
                              onClick={() => {
                                void detectMutation.mutateAsync(environment.id);
                              }}
                              disabled={detectMutation.isPending}
                              className="rounded-full border border-[var(--accent)]/30 bg-[var(--accent)]/10 px-3 py-1.5 text-xs font-semibold text-[var(--accent)] transition hover:bg-[var(--accent)]/15 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                              Detect
                            </button>
                            <button
                              type="button"
                              onClick={() => {
                                if (window.confirm(`Delete environment "${environment.alias}"?`)) {
                                  void deleteMutation.mutateAsync(environment.id);
                                }
                              }}
                              disabled={deleteMutation.isPending}
                              className="rounded-full border border-red-200 bg-red-50 px-3 py-1.5 text-xs font-semibold text-red-700 transition hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : null}
        </section>

        <EnvironmentEditor
          key={`${editorMode}-${editorEnvironmentId ?? 'new'}-${editorFormKey}`}
          mode={editorMode}
          environment={editorEnvironment}
          activeEnvironment={activeEnvironment}
          isSaving={saveMutation.isPending}
          onSubmit={async (values) => {
            await saveMutation.mutateAsync(values);
          }}
          onCancel={() => {
            if (editorMode === 'edit') {
              setEditorFormKey((value) => value + 1);
              setEditorMode('create');
              setEditorEnvironmentId(null);
              return;
            }
            setEditorFormKey((value) => value + 1);
            setEditorEnvironmentId(null);
          }}
        />
      </div>
    </div>
  );
}

export default ContainersPage;
