export type ReviewAction = 'CONCUR' | 'OVERRIDE' | 'REQUEST_RESCAN';

export interface ReviewSubmissionPayload {
  action: ReviewAction;
  notes: string;
  reviewerId: string;
  signedAt: string;
  evidenceVerifiedAcknowledgement: boolean;
  justification?: string;
}

export interface ReviewResponse {
  success: boolean;
  findingId: string;
  action: ReviewAction;
  recordedAt: string;
  reviewerId: string;
}
