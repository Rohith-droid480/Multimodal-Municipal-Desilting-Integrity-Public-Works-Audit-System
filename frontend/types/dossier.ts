import { AuditStatus, SeverityLevel } from './epistemic';

export type PriorityTier = 'P1_CRITICAL' | 'P2_HIGH' | 'P3_ELEVATED' | 'P4_ROUTINE';

export type BenchmarkCase = 'CLEAN_COMPLIANT' | 'SUBSTANTIVE_INCONSISTENCY' | 'INCONCLUSIVE_DATA';

export interface ContractorMetadata {
  contractorId: string;
  contractorName: string;
  contractNumber: string;
  workOrderNumber: string;
  workOrderDate: string;
  sanctionedAmountInr: number;
  wardNumber: string;
  reachName: string;
  drainId: string;
}

export interface DossierSummary {
  id: string;
  claimNumber: string;
  contractor: ContractorMetadata;
  financialExposureInr: number;
  /**
   * Evidence Consistency Score (ECS) [0, 1]:
   * Measures internal coherence across heterogeneous evidentiary artifacts.
   * NOT a fraud probability.
   */
  ecsScore: number;
  /**
   * Audit Review Priority Index (ARPI) [0, 100]:
   * Workload triage index to direct auditor attention.
   * NOT a legal guilt score.
   */
  arpiScore: number;
  priorityTier: PriorityTier;
  benchmarkCase: BenchmarkCase;
  status: AuditStatus;
  maxSeverity: SeverityLevel;
  evidenceCounts: {
    photos: number;
    receipts: number;
    trips: number;
    documents: number;
  };
  unresolvedFindingsCount: number;
  submittedAt: string;
  lastAuditedAt?: string;
}

export interface DossierListItem {
  id: string;
  claimNumber: string;
  wardNumber: string;
  workOrderNumber: string;
  contractorName: string;
  financialExposureInr: number;
  arpiScore: number;
  priorityTier: PriorityTier;
  ecsScore: number;
  status: AuditStatus;
  benchmarkCase: BenchmarkCase;
  submittedAt: string;
}
