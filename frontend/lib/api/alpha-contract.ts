/**
 * CANONICAL FROZEN ALPHA API CONTRACT SPECIFICATION
 * 
 * Version: Frozen Alpha Backend (commit 727b9e3)
 * Base URL: NEXT_PUBLIC_API_URL (default: http://localhost:8000)
 * 
 * Exact Endpoints:
 * - GET  /health
 * - GET  /dossiers/{id}
 * - GET  /dossiers/{id}/triage
 * - POST /dossiers/{id}/audit
 * - GET  /dossiers/{id}/visual-package
 * - GET  /dossiers/{id}/findings
 * - POST /findings/{id}/review
 * - GET  /dossiers/{id}/export/json
 * - GET  /dossiers/{id}/export/markdown
 * 
 * DO NOT INVENT ALTERNATIVE ENDPOINTS.
 */

export interface FrozenAlphaApiEndpoints {
  health: '/health';
  getDossier: '/dossiers/:id';
  getDossierTriage: '/dossiers/:id/triage';
  triggerAudit: '/dossiers/:id/audit';
  getVisualPackage: '/dossiers/:id/visual-package';
  getFindings: '/dossiers/:id/findings';
  submitReview: '/findings/:id/review';
  exportJson: '/dossiers/:id/export/json';
  exportMarkdown: '/dossiers/:id/export/markdown';
}
