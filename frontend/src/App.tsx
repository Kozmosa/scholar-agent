import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { ErrorBoundary, Layout, ToastProvider } from './components/common';
import DashboardPage from './pages/DashboardPage';
import PlaceholderPage from './pages/PlaceholderPage';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5000,
      refetchInterval: 10000,
    },
  },
});

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ToastProvider>
          <BrowserRouter>
            <Layout>
              <Routes>
                <Route path="/" element={<Navigate replace to="/terminal" />} />
                <Route path="/terminal" element={<DashboardPage />} />
                <Route
                  path="/workspaces"
                  element={
                    <PlaceholderPage
                      eyebrow="Workspaces"
                      title="Workspace orchestration is coming soon"
                      description="This area will expose project-specific workspaces, task context, and execution entrypoints once the runtime shell expands beyond Terminal."
                    />
                  }
                />
                <Route
                  path="/containers"
                  element={
                    <PlaceholderPage
                      eyebrow="Containers"
                      title="Container management is coming soon"
                      description="This area will surface runtime container state, environment preparation, and related controls after the terminal shell stabilizes."
                    />
                  }
                />
                <Route
                  path="/settings"
                  element={
                    <PlaceholderPage
                      eyebrow="Settings"
                      title="Settings are coming soon"
                      description="This area will host environment preferences, runtime configuration, and WebUI behavior controls in a later slice."
                    />
                  }
                />
              </Routes>
            </Layout>
          </BrowserRouter>
        </ToastProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;
