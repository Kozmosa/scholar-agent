import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';

interface Props {
  children: ReactNode;
}

function Layout({ children }: Props) {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="space-y-1">
            <Link to="/" className="text-lg font-semibold text-[var(--accent)]">
              Scholar Agent
            </Link>
            <p className="text-sm text-gray-600">
              Minimal frontend shell aligned to backend health checks, terminal bench controls,
              and the managed workspace browser.
            </p>
          </div>
        </div>
      </header>

      <main className="mx-auto flex-1 w-full max-w-5xl">{children}</main>

      <footer className="border-t border-gray-200 bg-white py-4 text-center text-sm text-gray-500">
        Health, terminal bench, and workspace browser shell during backend realignment.
      </footer>
    </div>
  );
}

export default Layout;
