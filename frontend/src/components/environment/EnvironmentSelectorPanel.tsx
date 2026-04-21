import type { EnvironmentRecord } from '../../types';
import { useT } from '../../i18n';

interface Props {
  environments: EnvironmentRecord[];
  selectedEnvironmentId: string | null;
  selectedEnvironment: EnvironmentRecord | null;
  isLoading: boolean;
  loadError: string | null;
  hasEnvironments: boolean;
  onSelectEnvironment: (environmentId: string) => void;
}

function EnvironmentSelectorPanel({
  environments,
  selectedEnvironmentId,
  selectedEnvironment,
  isLoading,
  loadError,
  hasEnvironments,
  onSelectEnvironment,
}: Props) {
  const t = useT();

  return (
    <section className="space-y-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="space-y-2">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--accent)]">
          {t('components.environmentSelector.eyebrow')}
        </p>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="space-y-1">
            <h2 className="text-xl font-semibold text-gray-900">
              {t('components.environmentSelector.title')}
            </h2>
            <p className="max-w-3xl text-sm text-gray-600">
              {t('components.environmentSelector.description')}
            </p>
          </div>
          <div className="rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-sm font-medium text-gray-700">
            {selectedEnvironment ? selectedEnvironment.alias : t('components.environmentSelector.selectedNone')}
          </div>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,0.8fr)_minmax(0,1.2fr)]">
        <label className="space-y-2">
          <span className="text-sm font-medium text-gray-900">
            {t('components.environmentSelector.activeLabel')}
          </span>
          <select
            value={selectedEnvironmentId ?? ''}
            onChange={(event) => onSelectEnvironment(event.target.value)}
            disabled={!hasEnvironments || isLoading}
            className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition focus:border-[var(--accent)] disabled:cursor-not-allowed disabled:bg-gray-100"
          >
            {!hasEnvironments ? <option value="">{t('components.environmentSelector.noAvailable')}</option> : null}
            {environments.map((environment) => (
              <option key={environment.id} value={environment.id}>
                {environment.alias} · {environment.display_name}
              </option>
            ))}
          </select>
        </label>

        <div className="space-y-2 rounded-2xl border border-gray-200 bg-gray-50 p-4">
          <div className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-gray-700">
            <span className="font-medium text-gray-900">{t('components.environmentSelector.selectionStatus')}</span>
            <span>
              {t('components.environmentSelector.loaded')} {isLoading ? t('common.no') : t('common.yes')}
            </span>
            <span>
              {t('components.environmentSelector.available')} {environments.length}
            </span>
          </div>

          {loadError ? (
            <p className="text-sm text-red-700">
              {t('components.environmentSelector.loadError')} {loadError}
            </p>
          ) : null}

          {selectedEnvironment ? (
            <div className="space-y-1 text-sm text-gray-700">
              <p>
                <span className="font-medium text-gray-900">
                  {t('components.environmentSelector.displayName')}
                </span>{' '}
                {selectedEnvironment.display_name}
              </p>
              <p>
                <span className="font-medium text-gray-900">{t('components.environmentSelector.host')}</span>{' '}
                {selectedEnvironment.host}
                :{selectedEnvironment.port}
              </p>
              <p>
                <span className="font-medium text-gray-900">
                  {t('components.environmentSelector.defaultWorkdir')}
                </span>{' '}
                {selectedEnvironment.default_workdir ?? t('common.notConfigured')}
              </p>
            </div>
          ) : (
            <p className="text-sm text-gray-500">
              {hasEnvironments
                ? t('components.environmentSelector.waitingValidSelection')
                : t('components.environmentSelector.createPrompt')}
            </p>
          )}
        </div>
      </div>
    </section>
  );
}

export default EnvironmentSelectorPanel;
