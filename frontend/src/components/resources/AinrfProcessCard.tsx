import type { ProcessInfo } from '../../types';
import { useT } from '../../i18n';

interface AinrfProcessCardProps {
  processes: ProcessInfo[];
  environmentName: string;
}

function formatRuntime(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  }
  if (minutes > 0) {
    return `${minutes}m ${secs}s`;
  }
  return `${secs}s`;
}

export default function AinrfProcessCard({ processes, environmentName }: AinrfProcessCardProps) {
  const t = useT();

  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-5">
      <h3 className="mb-4 text-sm font-semibold">
        {t('pages.resources.processCard.title')} — {environmentName}
      </h3>

      {processes.length === 0 ? (
        <p className="text-sm text-[var(--text-tertiary)]">{t('pages.resources.processCard.empty')}</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-[var(--border)] text-[var(--text-tertiary)]">
                <th className="pb-2 pr-4 font-medium">{t('pages.resources.processCard.columns.pid')}</th>
                <th className="pb-2 pr-4 font-medium">{t('pages.resources.processCard.columns.name')}</th>
                <th className="pb-2 pr-4 font-medium">{t('pages.resources.processCard.columns.cpu')}</th>
                <th className="pb-2 pr-4 font-medium">{t('pages.resources.processCard.columns.memory')}</th>
                <th className="pb-2 font-medium">{t('pages.resources.processCard.columns.runtime')}</th>
              </tr>
            </thead>
            <tbody>
              {[...processes].sort((a, b) => b.cpuPercent - a.cpuPercent).map((proc) => (
                <tr key={proc.pid} className="border-b border-[var(--border)]/50 last:border-0">
                  <td className="py-2 pr-4 font-mono">{proc.pid}</td>
                  <td className="py-2 pr-4">{proc.name}</td>
                  <td className="py-2 pr-4">{proc.cpuPercent.toFixed(1)}%</td>
                  <td className="py-2 pr-4">{proc.memoryMB} MB</td>
                  <td className="py-2">{formatRuntime(proc.runtimeSeconds)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
