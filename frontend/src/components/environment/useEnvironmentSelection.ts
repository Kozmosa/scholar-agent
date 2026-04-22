import { useEffect, useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getEnvironments, getProjectEnvironmentReferences } from '../../api';
import type { EnvironmentRecord, ProjectEnvironmentReference } from '../../types';

const environmentSelectionStorageKey = 'scholar-agent:selected-environment-id';
const defaultProjectId = 'default';
const EMPTY_ENVIRONMENTS: EnvironmentRecord[] = [];
const EMPTY_PROJECT_REFERENCES: ProjectEnvironmentReference[] = [];

function readStoredEnvironmentId(): string | null {
  try {
    return window.localStorage.getItem(environmentSelectionStorageKey);
  } catch {
    return null;
  }
}

function writeStoredEnvironmentId(environmentId: string | null): void {
  try {
    if (environmentId === null) {
      window.localStorage.removeItem(environmentSelectionStorageKey);
      return;
    }

    window.localStorage.setItem(environmentSelectionStorageKey, environmentId);
  } catch {
    // Ignore storage failures and keep the selection in memory.
  }
}

function resolveEnvironmentSelection(
  selectedEnvironmentId: string | null,
  environments: EnvironmentRecord[],
  projectReferences: ProjectEnvironmentReference[]
): string | null {
  if (environments.length === 0) {
    return null;
  }

  const projectDefaultReference =
    projectReferences.find((reference) => reference.is_default) ?? null;
  const projectDefaultEnvironment =
    projectDefaultReference !== null
      ? environments.find((environment) => environment.id === projectDefaultReference.environment_id) ??
        null
      : null;
  if (projectDefaultEnvironment !== null) {
    return projectDefaultEnvironment.id;
  }

  const storedEnvironment = selectedEnvironmentId
    ? environments.find((environment) => environment.id === selectedEnvironmentId) ?? null
    : null;
  if (storedEnvironment !== null) {
    return storedEnvironment.id;
  }

  const defaultEnvironment = environments.find((environment) => environment.is_seed);
  if (defaultEnvironment !== undefined) {
    return defaultEnvironment.id;
  }

  return environments[0]?.id ?? null;
}

export interface EnvironmentSelectionState {
  environments: EnvironmentRecord[];
  projectReferences: ProjectEnvironmentReference[];
  projectDefaultEnvironmentId: string | null;
  selectedEnvironmentId: string | null;
  selectedEnvironment: EnvironmentRecord | null;
  isLoading: boolean;
  loadError: string | null;
  hasEnvironments: boolean;
  onSelectEnvironment: (environmentId: string) => void;
}

export function useEnvironmentSelection(): EnvironmentSelectionState {
  const environmentsQuery = useQuery({
    queryKey: ['environments'],
    queryFn: getEnvironments,
  });
  const projectReferencesQuery = useQuery({
    queryKey: ['project-environment-refs', defaultProjectId],
    queryFn: () => getProjectEnvironmentReferences(defaultProjectId),
  });
  const [storedEnvironmentId, setStoredEnvironmentId] = useState<string | null>(() =>
    readStoredEnvironmentId()
  );

  const environments = environmentsQuery.data?.items ?? EMPTY_ENVIRONMENTS;
  const projectReferences = projectReferencesQuery.data?.items ?? EMPTY_PROJECT_REFERENCES;
  const selectedEnvironmentId = useMemo(
    () => resolveEnvironmentSelection(storedEnvironmentId, environments, projectReferences),
    [environments, projectReferences, storedEnvironmentId]
  );

  useEffect(() => {
    if (storedEnvironmentId === null || environments.length === 0) {
      return;
    }

    const storedEnvironmentStillExists = environments.some(
      (environment) => environment.id === storedEnvironmentId
    );
    if (storedEnvironmentStillExists) {
      return;
    }

    writeStoredEnvironmentId(selectedEnvironmentId);
  }, [environments, selectedEnvironmentId, storedEnvironmentId]);

  const selectedEnvironment = useMemo(
    () => environments.find((environment) => environment.id === selectedEnvironmentId) ?? null,
    [environments, selectedEnvironmentId]
  );

  const projectDefaultEnvironmentId =
    projectReferences.find((reference) => reference.is_default)?.environment_id ?? null;
  const loadError = [environmentsQuery.error, projectReferencesQuery.error]
    .filter((error): error is Error => error instanceof Error)
    .map((error) => error.message)
    .join(' | ') || null;

  const onSelectEnvironment = (environmentId: string): void => {
    setStoredEnvironmentId(environmentId);
    writeStoredEnvironmentId(environmentId);
  };

  return {
    environments,
    projectReferences,
    projectDefaultEnvironmentId,
    selectedEnvironmentId,
    selectedEnvironment,
    isLoading: environmentsQuery.isLoading || projectReferencesQuery.isLoading,
    loadError,
    hasEnvironments: environments.length > 0,
    onSelectEnvironment,
  };
}
