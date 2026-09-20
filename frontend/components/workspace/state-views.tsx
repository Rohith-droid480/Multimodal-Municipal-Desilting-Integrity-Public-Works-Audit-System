import React from 'react';
import { EpistemicBadge } from '@/components/ui/epistemic-badge';
import { 
  Inbox, 
  Loader2, 
  ShieldAlert, 
  HelpCircle, 
  AlertCircle, 
  RefreshCw 
} from 'lucide-react';

/**
 * EmptyState: Displayed when no active dossiers or findings exist in triage.
 */
export const EmptyState: React.FC<{ message?: string }> = ({
  message = "No audit dossiers currently awaiting triage.",
}) => (
  <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-app-bg text-slate-400">
    <Inbox className="w-12 h-12 text-slate-600 mb-3" />
    <h3 className="text-sm font-semibold text-slate-200">Queue Clean</h3>
    <p className="text-xs text-slate-500 max-w-sm mt-1">{message}</p>
  </div>
);

/**
 * LoadingState: Explicit loading spinner with step description.
 */
export const LoadingState: React.FC<{ step?: string }> = ({
  step = "Loading evidence artifacts and cross-verification signals...",
}) => (
  <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-app-bg text-slate-400 font-mono">
    <Loader2 className="w-10 h-10 text-sky-400 animate-spin mb-3" />
    <span className="text-xs text-slate-300 font-medium">{step}</span>
  </div>
);

/**
 * TechnicalAbstentionView: Renders explicit technical abstention state.
 * Core Rule: Missing evidence must NEVER be treated as proof of wrongdoing.
 */
export const TechnicalAbstentionView: React.FC<{ reason: string }> = ({ reason }) => (
  <div className="p-4 bg-zinc-950/80 rounded-lg border border-zinc-700 text-zinc-300 font-mono text-xs space-y-2">
    <div className="flex items-center gap-2">
      <EpistemicBadge technicalState="TECHNICAL_ABSTENTION" />
      <span className="font-semibold text-slate-200">System Abstention</span>
    </div>
    <p className="text-xs text-zinc-400 font-sans leading-relaxed">
      {reason}
    </p>
    <div className="text-[11px] text-zinc-500 pt-1 border-t border-zinc-800">
      Note: Technical abstentions reflect sensor, boundary, or evidentiary limitations and must not be interpreted as contractor guilt or fraud.
    </div>
  </div>
);

/**
 * InconclusiveDataView: Renders inconclusive state when evidence is degraded.
 */
export const InconclusiveDataView: React.FC<{ details: string }> = ({ details }) => (
  <div className="p-4 bg-slate-900 rounded-lg border border-slate-700 text-slate-300 font-mono text-xs space-y-2">
    <div className="flex items-center gap-2">
      <EpistemicBadge technicalState="INCONCLUSIVE_DATA" />
      <span className="font-semibold text-slate-200">Inconclusive Evidence</span>
    </div>
    <p className="text-xs text-slate-400 font-sans leading-relaxed">
      {details}
    </p>
  </div>
);
