import type { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';

interface Props {
  children: ReactNode;
}

function Layout({ children }: Props) {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/tasks', label: 'Tasks' },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="text-lg font-bold text-[var(--accent)]">
            Scholar Agent
          </Link>
          <nav className="flex gap-4">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-3 py-1 rounded ${
                  location.pathname === item.path
                    ? 'bg-[var(--accent-bg)] text-[var(--accent)]'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-6xl mx-auto w-full">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 py-4 text-center text-sm text-gray-500">
        Scholar Agent Dashboard
      </footer>
    </div>
  );
}

export default Layout;