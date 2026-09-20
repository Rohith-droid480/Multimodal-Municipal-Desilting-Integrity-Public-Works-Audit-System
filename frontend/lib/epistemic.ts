import { EpistemicCategory, SeverityLevel, TechnicalState, AuditStatus } from '@/types/epistemic';

export interface EpistemicConfig {
  label: string;
  badgeClass: string;
  iconName: string;
  description: string;
}

export const EPISTEMIC_CONFIG: Record<EpistemicCategory, EpistemicConfig> = {
  FACT: {
    label: 'FACT',
    badgeClass: 'bg-sky-950/80 text-sky-300 border-sky-600/60',
    iconName: 'Database',
    description: 'Directly extracted observation or verified ground truth from source evidence',
  },
  MODEL_OUTPUT: {
    label: 'MODEL OUTPUT',
    badgeClass: 'bg-purple-950/80 text-purple-300 border-purple-600/60',
    iconName: 'Cpu',
    description: 'Probabilistic prediction, embedding similarity, or machine-learning inference',
  },
  RULE_RESULT: {
    label: 'RULE RESULT',
    badgeClass: 'bg-amber-950/80 text-amber-300 border-amber-600/60',
    iconName: 'Scale',
    description: 'Deterministic arithmetic, physical constraint, or temporal invariant evaluation',
  },
  INFERENCE: {
    label: 'INFERENCE',
    badgeClass: 'bg-blue-950/80 text-blue-300 border-blue-600/60',
    iconName: 'Network',
    description: 'Corroborated relationship derived across multiple independent evidence sources',
  },
  RECOMMENDATION: {
    label: 'RECOMMENDATION',
    badgeClass: 'bg-emerald-950/80 text-emerald-300 border-emerald-600/60',
    iconName: 'CheckCircle2',
    description: 'Actionable guidance prioritized for human auditor review and adjudication',
  },
};

export const TECHNICAL_STATE_CONFIG: Record<TechnicalState, EpistemicConfig> = {
  INCONCLUSIVE_DATA: {
    label: 'INCONCLUSIVE DATA',
    badgeClass: 'bg-slate-900 text-slate-300 border-slate-600',
    iconName: 'HelpCircle',
    description: 'Available evidence is degraded, partial, or insufficient to evaluate definitively',
  },
  INSUFFICIENT_DATA: {
    label: 'INSUFFICIENT DATA',
    badgeClass: 'bg-slate-900 text-slate-300 border-slate-600',
    iconName: 'FileQuestion',
    description: 'Required evidence artifact was not submitted in the dossier',
  },
  TECHNICAL_ABSTENTION: {
    label: 'TECHNICAL ABSTENTION',
    badgeClass: 'bg-zinc-900 text-zinc-300 border-zinc-600',
    iconName: 'ShieldAlert',
    description: 'System explicitly abstained from scoring due to boundary violation or sensor limits',
  },
  FAILED: {
    label: 'PROCESSING FAILED',
    badgeClass: 'bg-red-950/80 text-red-300 border-red-700/70',
    iconName: 'XCircle',
    description: 'Automated processing pipeline encountered an unrecoverable technical error',
  },
  RETRYABLE: {
    label: 'RETRYABLE',
    badgeClass: 'bg-amber-950/60 text-amber-300 border-amber-600/50',
    iconName: 'RefreshCw',
    description: 'Transient failure; may be re-queued without changing dossier contents',
  },
  REVIEW_REQUIRED: {
    label: 'REVIEW REQUIRED',
    badgeClass: 'bg-orange-950/80 text-orange-300 border-orange-600/70',
    iconName: 'AlertCircle',
    description: 'Requires human verification before administrative decision or bill pass',
  },
};

export const SEVERITY_CONFIG: Record<SeverityLevel, EpistemicConfig> = {
  CRITICAL: {
    label: 'CRITICAL',
    badgeClass: 'bg-red-950/90 text-red-200 border-red-500',
    iconName: 'AlertOctagon',
    description: 'Direct contradictory evidence or severe contractual violation detected',
  },
  HIGH: {
    label: 'HIGH',
    badgeClass: 'bg-orange-950/90 text-orange-200 border-orange-500',
    iconName: 'AlertTriangle',
    description: 'Substantial inconsistency or high anomaly score requiring prioritized review',
  },
  MEDIUM: {
    label: 'MEDIUM',
    badgeClass: 'bg-amber-950/80 text-amber-200 border-amber-500',
    iconName: 'AlertCircle',
    description: 'Minor variance or moderate confidence threshold departure',
  },
  INCONCLUSIVE: {
    label: 'INCONCLUSIVE',
    badgeClass: 'bg-slate-900 text-slate-300 border-slate-600',
    iconName: 'HelpCircle',
    description: 'Degraded signal or unresolvable technical artifact; not evidence of wrongdoing',
  },
  CLEAN: {
    label: 'VERIFIED',
    badgeClass: 'bg-emerald-950/80 text-emerald-200 border-emerald-500',
    iconName: 'ShieldCheck',
    description: 'Evidence components are mutually consistent and satisfy validation checks',
  },
};

export const AUDIT_STATUS_CONFIG: Record<AuditStatus, EpistemicConfig> = {
  PENDING_AUDIT: {
    label: 'PENDING AUDIT',
    badgeClass: 'bg-slate-900 text-slate-400 border-slate-700',
    iconName: 'Clock',
    description: 'Awaiting initial triage by audit officer',
  },
  UNDER_REVIEW: {
    label: 'UNDER REVIEW',
    badgeClass: 'bg-blue-950 text-blue-300 border-blue-600',
    iconName: 'FileSearch',
    description: 'Actively being inspected in the forensic workspace',
  },
  VERIFIED_COMPLIANT: {
    label: 'VERIFIED COMPLIANT',
    badgeClass: 'bg-emerald-950 text-emerald-300 border-emerald-600',
    iconName: 'CheckCircle2',
    description: 'Evidence reviewed and verified internally consistent',
  },
  SUBSTANTIVE_INCONSISTENCY: {
    label: 'SUBSTANTIVE INCONSISTENCY',
    badgeClass: 'bg-red-950 text-red-300 border-red-600',
    iconName: 'AlertTriangle',
    description: 'Unreconciled objective contradiction found in contractor submission',
  },
  TECHNICAL_ABSTENTION: {
    label: 'TECHNICAL ABSTENTION',
    badgeClass: 'bg-zinc-900 text-zinc-300 border-zinc-600',
    iconName: 'ShieldAlert',
    description: 'Automated adjudication abstained due to missing or corrupt evidence',
  },
};
