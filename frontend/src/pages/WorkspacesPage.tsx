import { CodeServerCard, EnvironmentSelectorPanel, useEnvironmentSelection } from '../components';
import { useT } from '../i18n';

function WorkspacesPage() {
  const t = useT();
  const environmentSelection = useEnvironmentSelection();

  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <section className="mb-8 space-y-3">
        <p className="text-sm font-medium uppercase tracking-wide text-[var(--accent)]">
          {t('pages.workspaces.eyebrow')}
        </p>
        <h1 className="text-3xl font-semibold text-gray-900">{t('pages.workspaces.title')}</h1>
        <p className="max-w-3xl text-sm text-gray-600 sm:text-base">
          {t('pages.workspaces.description')}
        </p>
      </section>

      <section className="space-y-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <EnvironmentSelectorPanel {...environmentSelection} />
        <CodeServerCard selectedEnvironment={environmentSelection.selectedEnvironment} />
      </section>
    </div>
  );
}

export default WorkspacesPage;
