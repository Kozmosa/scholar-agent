function formatMB(mb: number): string {
  if (mb >= 1024) {
    return `${(mb / 1024).toFixed(1)} GB`;
  }
  return `${mb} MB`;
}

interface MemoryBarProps {
  usedMB: number;
  totalMB: number;
}

export default function MemoryBar({ usedMB, totalMB }: MemoryBarProps) {
  const percent = totalMB > 0 ? Math.round((usedMB / totalMB) * 100) : 0;

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs">
        <span className="font-medium">Memory</span>
        <span className="text-[var(--text-tertiary)]">
          {formatMB(usedMB)} / {formatMB(totalMB)} ({percent}%)
        </span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-[var(--bg-tertiary)]">
        <div
          className="h-full rounded-full bg-blue-500 transition-all duration-500"
          style={{ width: `${Math.min(percent, 100)}%` }}
        />
      </div>
    </div>
  );
}
