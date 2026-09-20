/**
 * Epistemic visual language and technical state definitions for MuniAudit-AI.
 * Non-negotiable invariant: Color alone must NEVER communicate meaning.
 * Always pair color + icon + text.
 */

export type EpistemicCategory = 
  | 'FACT' 
  | 'MODEL_OUTPUT' 
  | 'RULE_RESULT' 
  | 'INFERENCE' 
  | 'RECOMMENDATION';

export type TechnicalState =
  | 'INCONCLUSIVE_DATA'
  | 'INSUFFICIENT_DATA'
  | 'TECHNICAL_ABSTENTION'
  | 'FAILED'
  | 'RETRYABLE'
  | 'REVIEW_REQUIRED';

export type SeverityLevel =
  | 'CRITICAL'
  | 'HIGH'
  | 'MEDIUM'
  | 'INCONCLUSIVE'
  | 'CLEAN';

export type AuditStatus =
  | 'PENDING_AUDIT'
  | 'UNDER_REVIEW'
  | 'VERIFIED_COMPLIANT'
  | 'SUBSTANTIVE_INCONSISTENCY'
  | 'TECHNICAL_ABSTENTION';

export interface EpistemicMetadata {
  category: EpistemicCategory;
  sourceRef: string;
  confidence?: number;
  uncertaintyDescription?: string;
  timestamp: string;
}
