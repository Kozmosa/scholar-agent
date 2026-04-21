import { Boxes, ChevronLeft, ChevronRight, FolderKanban, Settings, SquareTerminal } from 'lucide-react';
import type { ReactNode } from 'react';
import { useMemo, useState } from 'react';
import { NavLink } from 'react-router-dom';

interface Props {
  children: ReactNode;
}

interface NavigationItem {
  label: string;
  to: string;
  description: string;
  icon: typeof SquareTerminal;
}

const navigationItems: NavigationItem[] = [
  {
    label: 'Terminal',
    to: '/terminal',
    description: 'Health checks and terminal bench access',
    icon: SquareTerminal,
  },
  {
    label: 'Workspaces',
    to: '/workspaces',
    description: 'Project workspaces and task context',
    icon: FolderKanban,
  },
  {
    label: 'Containers',
    to: '/containers',
    description: 'Runtime environments and container status',
    icon: Boxes,
  },
  {
    label: 'Settings',
    to: '/settings',
    description: 'Runtime and WebUI preferences',
    icon: Settings,
  },
];

function Layout({ children }: Props) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const asideWidth = useMemo(() => (isCollapsed ? 'w-20' : 'w-72'), [isCollapsed]);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <div className="flex min-h-screen">
        <aside
          className={`${asideWidth} flex shrink-0 flex-col border-r border-gray-200 bg-white/95 px-3 py-4 shadow-sm transition-all duration-200`}
        >
          <div className="flex items-start justify-between gap-3 px-2">
            <div className={isCollapsed ? 'hidden' : 'block'}>
              <p className="text-lg font-semibold text-[var(--accent)]">Scholar Agent</p>
              <p className="mt-1 text-sm text-gray-600">
                Minimal frontend shell aligned to backend health checks, terminal bench controls,
                the environment control plane, and the managed workspace browser.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setIsCollapsed((value) => !value)}
              className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-gray-200 bg-gray-50 text-gray-600 transition hover:border-[var(--accent)]/30 hover:text-[var(--accent)]"
              aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            >
              {isCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
            </button>
          </div>

          <nav className="mt-6 flex flex-1 flex-col gap-2">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    [
                      'group flex items-center gap-3 rounded-2xl border px-3 py-3 transition',
                      isCollapsed ? 'justify-center' : '',
                      isActive
                        ? 'border-[var(--accent)]/20 bg-[var(--accent)]/10 text-[var(--accent)] shadow-sm'
                        : 'border-transparent text-gray-600 hover:border-gray-200 hover:bg-gray-100 hover:text-gray-900',
                    ].join(' ')
                  }
                  title={isCollapsed ? item.label : undefined}
                >
                  <Icon size={18} className="shrink-0" />
                  {isCollapsed ? null : (
                    <span className="min-w-0">
                      <span className="block text-sm font-medium">{item.label}</span>
                      <span className="block text-xs text-gray-500">{item.description}</span>
                    </span>
                  )}
                </NavLink>
              );
            })}
          </nav>
        </aside>

        <div className="flex min-h-screen min-w-0 flex-1 flex-col">
          <header className="border-b border-gray-200 bg-white/80 px-4 py-4 backdrop-blur sm:px-6 lg:px-8">
            <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-6">
              <div>
                <p className="text-sm font-medium uppercase tracking-wide text-[var(--accent)]">
                  WebUI control surface
                </p>
                <p className="mt-1 text-sm text-gray-600">
                  Health, terminal bench, environment control plane, and workspace browser shell
                  during backend realignment.
                </p>
              </div>
            </div>
          </header>

          <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col">{children}</main>

          <footer className="border-t border-gray-200 bg-white/80 px-4 py-4 text-sm text-gray-500 sm:px-6 lg:px-8">
            <div className="mx-auto w-full max-w-6xl">
              Health, terminal bench, environment control plane, and workspace browser shell during
              backend realignment.
            </div>
          </footer>
        </div>
      </div>
    </div>
  );
}

export default Layout;
