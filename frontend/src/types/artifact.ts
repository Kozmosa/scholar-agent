// Artifact Preview Contract Types
// Based on docs/LLM-Working/refactoring-plan/artifact-preview-contract.md

export type ArtifactType = 'table' | 'report' | 'figure';
export type PreviewFormat = 'csv' | 'markdown' | 'svg' | 'png';

export interface ArtifactPreview {
  artifact_id: string;
  artifact_type: ArtifactType;
  display_title: string;
  preview_format: PreviewFormat;
  preview_ref: string;
  created_at?: string;
}

// For list display (minimal)
export interface ArtifactListItem {
  artifact_id: string;
  artifact_type: ArtifactType;
  display_title: string;
  preview_format: PreviewFormat;
}