import type { ResourceSnapshot as ResourceSnapshotType } from '../../types';

interface Props {
  snapshot: ResourceSnapshotType | undefined;
  isLoading: boolean;
}

function ResourceSnapshot({ snapshot, isLoading }: Props) {
  if (isLoading) {
    return <div className="text-gray-500">Loading resources...</div>;
  }

  if (!snapshot) {
    return <div className="text-gray-500">Unable to fetch resources</div>;
  }

  const formatPercent = (value: number | null) => {
    if (value === null) return 'N/A';
    return `${Math.round(value)}%`;
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div className="p-3 rounded bg-gray-50 border border-gray-200">
        <div className="text-sm text-gray-500">GPU</div>
        <div className="text-lg font-semibold">{formatPercent(snapshot.gpu)}</div>
      </div>
      <div className="p-3 rounded bg-gray-50 border border-gray-200">
        <div className="text-sm text-gray-500">CPU</div>
        <div className="text-lg font-semibold">{formatPercent(snapshot.cpu)}</div>
      </div>
      <div className="p-3 rounded bg-gray-50 border border-gray-200">
        <div className="text-sm text-gray-500">Memory</div>
        <div className="text-lg font-semibold">{formatPercent(snapshot.memory)}</div>
      </div>
      <div className="p-3 rounded bg-gray-50 border border-gray-200">
        <div className="text-sm text-gray-500">Disk</div>
        <div className="text-lg font-semibold">{formatPercent(snapshot.disk)}</div>
      </div>
    </div>
  );
}

export default ResourceSnapshot;