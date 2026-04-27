import {
  Boxes,
  ChevronLeft,
  ChevronRight,
  FolderKanban,
  ListChecks,
  Settings,
  SquareTerminal,
} from 'lucide-react';
import type { ReactNode } from 'react';
import { useMemo, useState } from 'react';
import { NavLink } from 'react-router-dom';
import LocaleSwitcher from './LocaleSwitcher';
import { useT } from '../../i18n';

interface Props {
  children: ReactNode;
  edgeToEdge?: boolean;
}

interface NavigationItem {
  label: string;
  to: string;
  description: string;
  icon: typeof SquareTerminal;
}

function Layout({ children, edgeToEdge = false }: Props) {
  const t = useT();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const asideWidth = useMemo(() => (isCollapsed ? 'w-[56px]' : 'w-[248px]'), [isCollapsed]);
  const navigationItems: NavigationItem[] = [
    {
      label: t('navigation.terminal.label'),
      to: '/terminal',
      description: t('navigation.terminal.description'),
      icon: SquareTerminal,
    },
    {
      label: t('navigation.tasks.label'),
      to: '/tasks',
      description: t('navigation.tasks.description'),
      icon: ListChecks,
    },
    {
      label: t('navigation.workspaces.label'),
      to: '/workspaces',
      description: t('navigation.workspaces.description'),
      icon: FolderKanban,
    },
    {
      label: t('navigation.containers.label'),
      to: '/containers',
      description: t('navigation.containers.description'),
      icon: Boxes,
    },
    {
      label: t('navigation.settings.label'),
      to: '/settings',
      description: t('navigation.settings.description'),
      icon: Settings,
    },
  ];

  return (
    <div className="min-h-screen bg-[var(--background)] text-[var(--foreground)]">
      <div className="flex min-h-screen">
        <aside
          className={`${asideWidth} flex shrink-0 flex-col border-r border-[var(--sidebar-border)] bg-[var(--sidebar)] text-[var(--sidebar-foreground)] transition-all duration-200 ease-out`}
        >
          <div className="flex h-12 items-center justify-between border-b border-[var(--sidebar-border)] px-3">
            {!isCollapsed && (
              <div className="min-w-0">
                <p className="truncate text-sm font-semibold tracking-tight">{t('common.appName')}</p>
                <p className="truncate text-[11px] text-[var(--text-tertiary)]">AINRF console</p>
              </div>
            )}
            <button
              type="button"
              onClick={() => setIsCollapsed((value) => !value)}
              className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-[var(--muted-foreground)] transition hover:bg-[var(--sidebar-primary)] hover:text-[var(--sidebar-foreground)]"
              aria-label={isCollapsed ? t('layout.expandSidebar') : t('layout.collapseSidebar')}
            >
              {isCollapsed ? <ChevronRight size={15} /> : <ChevronLeft size={15} />}
            </button>
          </div>

          <nav className="flex flex-1 flex-col gap-1 px-2 py-3">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    [
                      'group flex items-center gap-3 rounded-lg px-2.5 py-2 text-sm transition',
                      isCollapsed ? 'justify-center' : '',
                      isActive
                        ? 'bg-[var(--sidebar-primary)] text-[var(--sidebar-primary-foreground)] shadow-[var(--shadow-toolbar)]'
                        : 'text-[var(--muted-foreground)] hover:bg-[var(--sidebar-primary)] hover:text-[var(--sidebar-foreground)]',
                    ].join(' ')
                  }
                  title={isCollapsed ? item.label : undefined}
                >
                  <Icon size={17} className="shrink-0" strokeWidth={1.7} />
                  {isCollapsed ? null : (
                    <span className="min-w-0">
                      <span className="block truncate font-medium leading-tight">{item.label}</span>
                      <span className="block truncate text-[11px] leading-relaxed text-[var(--text-tertiary)]">
                        {item.description}
                      </span>
                    </span>
                  )}
                </NavLink>
              );
            })}
          </nav>

          {!isCollapsed && (
            <div className="border-t border-[var(--sidebar-border)] px-3 py-3">
              <p className="text-[11px] leading-relaxed text-[var(--text-tertiary)]">
                {t('layout.brandLine')}
              </p>
            </div>
          )}
        </aside>

        <div className="flex min-h-screen min-w-0 flex-1 flex-col">
          <header className="sticky top-0 z-40 flex h-12 items-center justify-between border-b border-[var(--border)] bg-[var(--background)]/85 px-4 backdrop-blur-xl">
            <div className="flex min-w-0 items-center gap-3">
              <p className="truncate text-xs font-medium uppercase tracking-wide text-[var(--muted-foreground)]">
                {t('layout.headerEyebrow')}
              </p>
              <span className="h-3 w-px bg-[var(--border)]" />
              <p className="truncate text-xs text-[var(--muted-foreground)]">
                {t('layout.headerDescription')}
              </p>
            </div>
            <LocaleSwitcher />
          </header>

          <main
            className={[
              'flex w-full flex-1 flex-col overflow-hidden',
              edgeToEdge ? '' : 'mx-auto max-w-[1100px] px-6 py-8',
            ].join(' ')}
          >
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}

export default Layout;
