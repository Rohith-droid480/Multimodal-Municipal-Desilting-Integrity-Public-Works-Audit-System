import { EpistemicCategory, SeverityLevel, TechnicalState } from './epistemic';

export type ModalityAttribution = 
  | 'DOCUMENT_INTELLIGENCE'
  | 'VISUAL_VERIFICATION'
  | 'GEOSPATIAL_TELEMETRY'
  | 'CROSS_MODAL';

export interface FindingCausalityChain {
  evidenceIds: string[];
  extractedFacts: Array<{
    label: string;
    value: string;
    sourceRef: string;
  }>;
  modelOutputs: Array<{
    modelName: string;
    outputKey: string;
    score: number;
    confidence: number;
    caveat?: string;
  }>;
  ruleResults: Array<{
    ruleId: string;
    ruleName: string;
    passed: boolean;
    expected: string;
    actual: string;
    deviation?: string;
  }>;
  inferences: Array<{
    statement: string;
    basis: string;
  }>;
  uncertaintyScore: number; // [0, 1] Subjective Logic uncertainty parameter 'u'
  recommendedHumanAction: string;
}

export interface FindingGagasElements {
  /** 1. Criteria: What should be (statutory standard, contract clause, physical law) */
  criteria: string;
  /** 2. Condition: What is (directly observed empirical fact) */
  condition: string;
  /** 3. Cause Hypothesis: Why it happened */
  causeHypothesis: string;
  /** 4. Effect: Impact or exposure (financial, operational, structural) */
  effect: string;
  /** 5. Recommendation: Corrective auditor action */
  recommendation: string;
}

export interface Finding {
  id: string;
  dossierId: string;
  title: string;
  description: string;
  category: EpistemicCategory;
  severity: SeverityLevel;
  technicalState?: TechnicalState;
  modality: ModalityAttribution;
  gagas: FindingGagasElements;
  causality: FindingCausalityChain;
  createdAt: string;
  reviewedBy?: string;
  reviewedAt?: string;
  reviewAction?: 'CONCUR' | 'OVERRIDE' | 'REQUEST_RESCAN';
  reviewerNotes?: string;
  overrideJustification?: string;
}
