import { useEffect, useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getEnvironments } from '../../api';
import type { EnvironmentRecord } from '../../types';

const environmentSelectionStorageKey = 'scholar-agent:selected-environment-id';
const EMPTY_ENVIRONMENTS: EnvironmentRecord[] = [];

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
  environments: EnvironmentRecord[]
): string | null {
  if (environments.length === 0) {
    return null;
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
  const [storedEnvironmentId, setStoredEnvironmentId] = useState<string | null>(() =>
    readStoredEnvironmentId()
  );

  const environments = environmentsQuery.data?.items ?? EMPTY_ENVIRONMENTS;
  const selectedEnvironmentId = useMemo(
    () => resolveEnvironmentSelection(storedEnvironmentId, environments),
    [environments, storedEnvironmentId]
  );

  useEffect(() => {
    writeStoredEnvironmentId(selectedEnvironmentId);
  }, [selectedEnvironmentId]);

  const selectedEnvironment = useMemo(
    () => environments.find((environment) => environment.id === selectedEnvironmentId) ?? null,
    [environments, selectedEnvironmentId]
  );

  const loadError =
    environmentsQuery.error instanceof Error ? environmentsQuery.error.message : null;

  const onSelectEnvironment = (environmentId: string): void => {
    setStoredEnvironmentId(environmentId);
    writeStoredEnvironmentId(environmentId);
  };

  return {
    environments,
    selectedEnvironmentId,
    selectedEnvironment,
    isLoading: environmentsQuery.isLoading,
    loadError,
    hasEnvironments: environments.length > 0,
    onSelectEnvironment,
  };
}
