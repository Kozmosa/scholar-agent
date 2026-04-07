import type { ArtifactListItem, ArtifactType } from '../../types';

interface Props {
  artifacts: ArtifactListItem[] | undefined;
  isLoading: boolean;
  onSelect?: (artifact: ArtifactListItem) => void;
}

const typeIcons: Record<ArtifactType, string> = {
  table: '📊',
  report: '📄',
  figure: '📈',
};

function RecentArtifacts({ artifacts, isLoading, onSelect }: Props) {
  if (isLoading) {
    return <div className="text-gray-500">Loading recent artifacts...</div>;
  }

  if (!artifacts || artifacts.length === 0) {
    return <div className="text-gray-500">No recent artifacts</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
      {artifacts.slice(0, 6).map((artifact) => (
        <button
          key={artifact.artifact_id}
          onClick={() => onSelect?.(artifact)}
          className="p-3 rounded border border-gray-200 hover:border-[var(--accent)] text-left"
          disabled={!onSelect}
        >
          <div className="flex items-center gap-2">
            <span>{typeIcons[artifact.artifact_type]}</span>
            <span className="font-medium">{artifact.display_title}</span>
          </div>
          <div className="text-sm text-gray-500 mt-1">
            {artifact.artifact_type} | {artifact.preview_format}
          </div>
        </button>
      ))}
    </div>
  );
}

export default RecentArtifacts;