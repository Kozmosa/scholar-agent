import type { ArtifactListItem } from '../../types';

interface Props {
  artifact: ArtifactListItem;
  content: { content: string; format: string } | undefined;
  isLoading: boolean;
  onClose: () => void;
}

function ArtifactPreviewModal({ artifact, content, isLoading, onClose }: Props) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-3xl max-h-[80vh] overflow-hidden shadow-lg">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 className="font-semibold">{artifact.display_title}</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-4 overflow-auto max-h-[60vh]">
          {isLoading ? (
            <div className="text-gray-500">Loading content...</div>
          ) : content ? (
            renderContent(artifact, content)
          ) : (
            <div className="text-red-500">Failed to load content</div>
          )}
        </div>
      </div>
    </div>
  );
}

function renderContent(artifact: ArtifactListItem, content: { content: string; format: string }) {
  const { artifact_type, preview_format } = artifact;

  switch (artifact_type) {
    case 'table':
      if (preview_format === 'csv') {
        return renderCSVTable(content.content);
      }
      return <pre className="whitespace-pre-wrap font-mono text-sm">{content.content}</pre>;

    case 'report':
      return <div className="prose max-w-none">{content.content}</div>;

    case 'figure':
      if (preview_format === 'png') {
        return (
          <img
            src={`data:image/png;base64,${content.content}`}
            alt={artifact.display_title}
            className="max-w-full"
          />
        );
      }
      // SVG or other
      return (
        <div
          dangerouslySetInnerHTML={{ __html: content.content }}
          className="max-w-full"
        />
      );

    default:
      return <pre className="whitespace-pre-wrap font-mono text-sm">{content.content}</pre>;
  }
}

function renderCSVTable(csv: string) {
  const lines = csv.trim().split('\n');
  if (lines.length === 0) return <div className="text-gray-500">Empty table</div>;

  const headers = lines[0].split(',');
  const rows = lines.slice(1).map((line) => line.split(','));

  return (
    <table className="w-full text-sm border-collapse">
      <thead>
        <tr>
          {headers.map((header, i) => (
            <th key={i} className="p-2 border border-gray-200 bg-gray-50 text-left">
              {header.trim()}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i}>
            {row.map((cell, j) => (
              <td key={j} className="p-2 border border-gray-200">
                {cell.trim()}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default ArtifactPreviewModal;