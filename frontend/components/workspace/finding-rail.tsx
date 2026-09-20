import React, { useState } from 'react';
import { Finding } from '@/types/finding';
import { ReviewAction } from '@/types/review';
import { EpistemicBadge } from '@/components/ui/epistemic-badge';
import { SeverityBadge } from '@/components/ui/severity-badge';
import { 
  AlertOctagon, 
  AlertTriangle, 
  HelpCircle, 
  CheckCircle2, 
  Cpu, 
  Scale, 
  ArrowRight, 
  UserCheck, 
  RotateCcw,
  FileCheck2,
  Info,
  Layers,
  BookOpen,
  CheckSquare,
  Square
} from 'lucide-react';

interface FindingRailProps {
  findings: Finding[];
  selectedFindingId: string | null;
  onSelectFinding: (id: string) => void;
  onAdjudicate: (
    findingId: string, 
    action: ReviewAction, 
    notes: string, 
    justification?: string
  ) => Promise<void>;
}

export const FindingRail: React.FC<FindingRailProps> = ({
  findings,
  selectedFindingId,
  onSelectFinding,
  onAdjudicate,
}) => {
  const [reviewNotes, setReviewNotes] = useState('');
  const [overrideJustification, setOverrideJustification] = useState('');
  const [selectedAction, setSelectedAction] = useState<ReviewAction>('CONCUR');
  const [evidenceAcknowledged, setEvidenceAcknowledged] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const activeFinding = findings.find((f) => f.id === selectedFindingId) || findings[0];

  const handleSubmitReview = async () => {
    if (!activeFinding || !evidenceAcknowledged || isSubmitting) return;

    if (selectedAction === 'OVERRIDE' && !overrideJustification.trim()) {
      return; // Override requires justification
    }

    setIsSubmitting(true);
    try {
      await onAdjudicate(
        activeFinding.id, 
        selectedAction, 
        reviewNotes, 
        selectedAction === 'OVERRIDE' ? overrideJustification : undefined
      );
      setReviewNotes('');
      setOverrideJustification('');
      setEvidenceAcknowledged(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <aside className="w-96 bg-app-surface border-l border-app-border flex flex-col shrink-0 overflow-y-auto" data-testid="finding-rail">
      {/* Header */}
      <div className="p-3 border-b border-app-border bg-app-surface/90 sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-mono font-semibold uppercase tracking-wider text-slate-300">
            Finding & Causality ({findings.length})
          </h2>
          <span className="text-[10px] font-mono text-slate-500">
            GAGAS / YELLOW BOOK
          </span>
        </div>
      </div>

      {/* Finding Selector Tabs */}
      <div className="p-3 border-b border-app-border space-y-1.5">
        {findings.map((f) => {
          const isSelected = f.id === activeFinding?.id;
          return (
            <button
              key={f.id}
              onClick={() => onSelectFinding(f.id)}
              className={`w-full text-left p-2.5 rounded border transition-all text-xs cursor-pointer ${
                isSelected
                  ? 'bg-app-active border-app-border-focus text-slate-100 shadow-xs'
                  : 'bg-app-elevated/40 border-app-border text-slate-300 hover:bg-app-elevated'
              }`}
              data-testid={`finding-item-${f.id}`}
            >
              <div className="flex items-center justify-between gap-1 mb-1">
                <SeverityBadge severity={f.severity} />
                <EpistemicBadge category={f.category} technicalState={f.technicalState} />
              </div>
              <p className="font-medium text-slate-200 line-clamp-1">{f.title}</p>
              {f.reviewedBy && (
                <div className="text-[10px] font-mono text-emerald-400 mt-1 flex items-center gap-1">
                  <CheckCircle2 className="w-2.5 h-2.5" />
                  <span>Adjudicated: {f.reviewAction || 'REVIEWED'}</span>
                </div>
              )}
            </button>
          );
        })}
      </div>

      {/* Active Finding Causality & GAGAS Breakdown */}
      {activeFinding && (
        <div className="p-4 space-y-4 text-xs font-sans">
          {/* Finding Title & Overview */}
          <div>
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span className="font-mono text-[11px] text-slate-400">
                {activeFinding.id}
              </span>
              <SeverityBadge severity={activeFinding.severity} />
              <EpistemicBadge 
                category={activeFinding.category} 
                technicalState={activeFinding.technicalState} 
              />
              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 border border-slate-700">
                {activeFinding.modality}
              </span>
            </div>
            <h3 className="text-sm font-semibold text-slate-100">
              {activeFinding.title}
            </h3>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              {activeFinding.description}
            </p>
          </div>

          {/* ================================================================= */}
          {/* 5 GAGAS Audit Elements (Criteria, Condition, Cause, Effect, Recommendation) */}
          {/* ================================================================= */}
          {activeFinding.gagas && (
            <div className="p-3 bg-app-elevated/70 rounded-lg border border-app-border space-y-2.5" data-testid="gagas-elements-box">
              <div className="flex items-center gap-1.5 text-slate-200 font-mono text-[11px] font-semibold uppercase border-b border-app-border pb-1">
                <BookOpen className="w-3.5 h-3.5 text-sky-400" />
                <span>GAGAS / Yellow Book Elements</span>
              </div>

              {/* 1. Criteria */}
              <div className="space-y-0.5">
                <div className="text-[10px] font-mono font-semibold uppercase text-slate-400">
                  1. Criteria (What Should Be):
                </div>
                <div className="text-slate-300 text-[11px] leading-relaxed">
                  {activeFinding.gagas.criteria}
                </div>
              </div>

              {/* 2. Condition */}
              <div className="space-y-0.5">
                <div className="text-[10px] font-mono font-semibold uppercase text-sky-400">
                  2. Condition (What Is):
                </div>
                <div className="text-slate-200 text-[11px] leading-relaxed font-mono bg-app-surface/60 p-1.5 rounded border border-app-border">
                  {activeFinding.gagas.condition}
                </div>
              </div>

              {/* 3. Cause Hypothesis */}
              <div className="space-y-0.5">
                <div className="text-[10px] font-mono font-semibold uppercase text-slate-400">
                  3. Cause Hypothesis:
                </div>
                <div className="text-slate-300 text-[11px] leading-relaxed">
                  {activeFinding.gagas.causeHypothesis}
                </div>
              </div>

              {/* 4. Effect */}
              <div className="space-y-0.5">
                <div className="text-[10px] font-mono font-semibold uppercase text-orange-400">
                  4. Effect (Exposure / Impact):
                </div>
                <div className="text-slate-200 text-[11px] leading-relaxed">
                  {activeFinding.gagas.effect}
                </div>
              </div>

              {/* 5. Recommendation */}
              <div className="space-y-0.5">
                <div className="text-[10px] font-mono font-semibold uppercase text-emerald-400">
                  5. Recommendation:
                </div>
                <div className="text-emerald-200 text-[11px] leading-relaxed font-semibold">
                  {activeFinding.gagas.recommendation}
                </div>
              </div>
            </div>
          )}

          {/* Extracted Facts, Model Outputs, Rule Results */}
          <div className="space-y-2">
            {/* Extracted Facts */}
            {activeFinding.causality.extractedFacts.length > 0 && (
              <div className="p-2.5 bg-app-elevated/40 rounded border border-app-border space-y-1">
                <div className="flex items-center gap-1.5 text-sky-400 font-mono text-[10px] font-semibold uppercase">
                  <EpistemicBadge category="FACT" />
                  <span>Extracted Observations</span>
                </div>
                <div className="space-y-1 font-mono text-[11px]">
                  {activeFinding.causality.extractedFacts.map((fact, idx) => (
                    <div key={idx} className="bg-app-surface/60 p-1 rounded border border-app-border">
                      <span className="text-slate-400">{fact.label}:</span>{' '}
                      <span className="text-slate-200 font-medium">{fact.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Model Outputs */}
            {activeFinding.causality.modelOutputs.length > 0 && (
              <div className="p-2.5 bg-app-elevated/40 rounded border border-app-border space-y-1">
                <div className="flex items-center gap-1.5 text-purple-400 font-mono text-[10px] font-semibold uppercase">
                  <EpistemicBadge category="MODEL_OUTPUT" />
                  <span>Probabilistic ML Signal</span>
                </div>
                <div className="space-y-1 font-mono text-[11px]">
                  {activeFinding.causality.modelOutputs.map((mo, idx) => (
                    <div key={idx} className="bg-app-surface/60 p-1 rounded border border-app-border">
                      <div className="flex items-center justify-between text-slate-300 font-medium">
                        <span>{mo.modelName}</span>
                        <span className="text-purple-300">{mo.outputKey}: {mo.score}</span>
                      </div>
                      {mo.caveat && (
                        <div className="text-[10px] text-slate-400 mt-0.5 italic">
                          * {mo.caveat}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Rule Results */}
            {activeFinding.causality.ruleResults.length > 0 && (
              <div className="p-2.5 bg-app-elevated/40 rounded border border-app-border space-y-1">
                <div className="flex items-center gap-1.5 text-amber-400 font-mono text-[10px] font-semibold uppercase">
                  <EpistemicBadge category="RULE_RESULT" />
                  <span>Deterministic Rule Result</span>
                </div>
                <div className="space-y-1 font-mono text-[11px]">
                  {activeFinding.causality.ruleResults.map((rule, idx) => (
                    <div key={idx} className="bg-app-surface/60 p-1 rounded border border-app-border">
                      <div className="flex items-center justify-between">
                        <span className="text-slate-300 font-medium">{rule.ruleName}</span>
                        <span className={`px-1 rounded text-[10px] ${rule.passed ? 'bg-emerald-950 text-emerald-300' : 'bg-red-950 text-red-300'}`}>
                          {rule.passed ? 'PASSED' : 'FAILED'}
                        </span>
                      </div>
                      <div className="text-[10px] text-slate-400 mt-0.5">
                        Expected: {rule.expected} | Actual: {rule.actual}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Uncertainty Score */}
          <div className="p-2 bg-app-elevated/40 rounded border border-app-border flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400 flex items-center gap-1 text-[11px]">
              <Info className="w-3 h-3 text-slate-500" />
              Epistemic Uncertainty (u):
            </span>
            <span className="font-bold text-slate-200">
              {(activeFinding.causality.uncertaintyScore * 100).toFixed(0)}%
            </span>
          </div>

          {/* ================================================================= */}
          {/* COGNITIVE REVIEW GATE: Mandatory Acknowledgement & Adjudication */}
          {/* ================================================================= */}
          <div className="p-3 bg-app-elevated rounded-lg border border-app-border space-y-3" data-testid="cognitive-review-gate">
            <div className="flex items-center justify-between border-b border-app-border pb-1.5">
              <div className="text-xs font-mono font-semibold text-slate-200 uppercase tracking-wider flex items-center gap-1">
                <UserCheck className="w-3.5 h-3.5 text-sky-400" />
                Cognitive Review Gate
              </div>
              <span className="text-[10px] font-mono text-slate-500">MANDATORY INSPECTION</span>
            </div>

            {/* If already reviewed, display existing audit adjudication record */}
            {activeFinding.reviewedBy ? (
              <div className="p-2.5 bg-app-surface rounded border border-emerald-800/80 space-y-1 font-mono text-[11px]">
                <div className="flex items-center justify-between text-emerald-400 font-bold">
                  <span>Adjudication: {activeFinding.reviewAction}</span>
                  <span className="text-[10px] text-slate-400">{activeFinding.reviewedBy}</span>
                </div>
                {activeFinding.reviewerNotes && (
                  <div className="text-slate-300 font-sans mt-1">
                    &ldquo;{activeFinding.reviewerNotes}&rdquo;
                  </div>
                )}
                {activeFinding.overrideJustification && (
                  <div className="text-amber-300 font-sans text-[10px] mt-1 p-1 bg-amber-950/40 rounded border border-amber-800">
                    <strong>Override Justification:</strong> {activeFinding.overrideJustification}
                  </div>
                )}
                <div className="text-[10px] text-slate-500 pt-1">
                  Recorded: {new Date(activeFinding.reviewedAt || '').toLocaleString('en-IN')}
                </div>
              </div>
            ) : (
              <div className="space-y-2.5">
                {/* Mandatory Primary Evidence Acknowledgement Checkbox */}
                <label className="flex items-start gap-2 p-2 bg-app-surface/80 rounded border border-app-border cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={evidenceAcknowledged}
                    onChange={(e) => setEvidenceAcknowledged(e.target.checked)}
                    className="mt-0.5 rounded border-slate-600 text-sky-600 focus:ring-sky-500 cursor-pointer"
                    data-testid="evidence-ack-checkbox"
                  />
                  <span className="text-[11px] text-slate-300 leading-snug font-sans">
                    I have personally inspected the primary source evidence artifacts (receipt scan / site photos / GPS logs) and verified the cross-modal observations before adjudicating.
                  </span>
                </label>

                {/* Review Action Selector (CONCUR, OVERRIDE, REQUEST_RESCAN) */}
                <div className="space-y-1">
                  <div className="text-[11px] font-mono text-slate-400 uppercase">
                    Adjudication Decision:
                  </div>
                  <div className="grid grid-cols-3 gap-1.5 font-mono text-[11px]">
                    <button
                      type="button"
                      onClick={() => setSelectedAction('CONCUR')}
                      className={`py-1.5 px-1 rounded border text-center transition-colors cursor-pointer ${
                        selectedAction === 'CONCUR'
                          ? 'bg-emerald-950 text-emerald-300 border-emerald-700 font-bold'
                          : 'bg-app-surface text-slate-400 border-app-border hover:bg-app-surface/90'
                      }`}
                      data-testid="action-concur-btn"
                    >
                      CONCUR
                    </button>
                    <button
                      type="button"
                      onClick={() => setSelectedAction('OVERRIDE')}
                      className={`py-1.5 px-1 rounded border text-center transition-colors cursor-pointer ${
                        selectedAction === 'OVERRIDE'
                          ? 'bg-red-950 text-red-300 border-red-700 font-bold'
                          : 'bg-app-surface text-slate-400 border-app-border hover:bg-app-surface/90'
                      }`}
                      data-testid="action-override-btn"
                    >
                      OVERRIDE
                    </button>
                    <button
                      type="button"
                      onClick={() => setSelectedAction('REQUEST_RESCAN')}
                      className={`py-1.5 px-1 rounded border text-center transition-colors cursor-pointer ${
                        selectedAction === 'REQUEST_RESCAN'
                          ? 'bg-amber-950 text-amber-300 border-amber-700 font-bold'
                          : 'bg-app-surface text-slate-400 border-app-border hover:bg-app-surface/90'
                      }`}
                      data-testid="action-rescan-btn"
                    >
                      RESCAN
                    </button>
                  </div>
                </div>

                {/* Override Justification (MANDATORY if OVERRIDE selected) */}
                {selectedAction === 'OVERRIDE' && (
                  <div className="space-y-1">
                    <div className="text-[11px] font-mono text-red-400 uppercase font-semibold">
                      Override Justification (Required):
                    </div>
                    <textarea
                      value={overrideJustification}
                      onChange={(e) => setOverrideJustification(e.target.value)}
                      placeholder="State substantive factual justification for overriding the system finding..."
                      className="w-full bg-app-surface border border-red-800 rounded p-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-hidden focus:border-red-500 h-16 resize-none font-sans"
                      data-testid="override-justification-input"
                    />
                  </div>
                )}

                {/* Auditor Remarks / Notes */}
                <div className="space-y-1">
                  <div className="text-[11px] font-mono text-slate-400 uppercase">
                    Auditor Remarks / Notice Instructions:
                  </div>
                  <textarea
                    value={reviewNotes}
                    onChange={(e) => setReviewNotes(e.target.value)}
                    placeholder="Enter official audit remarks or instructions for contractor notice..."
                    className="w-full bg-app-surface border border-app-border rounded p-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-hidden focus:border-sky-500 h-14 resize-none font-sans"
                    data-testid="review-notes-input"
                  />
                </div>

                {/* Submit Adjudication Button */}
                <button
                  type="button"
                  onClick={handleSubmitReview}
                  disabled={
                    !evidenceAcknowledged || 
                    isSubmitting || 
                    (selectedAction === 'OVERRIDE' && !overrideJustification.trim())
                  }
                  className="w-full bg-sky-950 hover:bg-sky-900 text-sky-200 border border-sky-800 py-2 px-3 rounded font-mono text-xs font-semibold transition-colors flex items-center justify-center gap-1.5 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
                  data-testid="submit-review-btn"
                >
                  <FileCheck2 className="w-3.5 h-3.5" />
                  <span>
                    {isSubmitting 
                      ? 'Submitting to POST /findings/{id}/review...' 
                      : `Submit ${selectedAction} Adjudication`}
                  </span>
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </aside>
  );
};
