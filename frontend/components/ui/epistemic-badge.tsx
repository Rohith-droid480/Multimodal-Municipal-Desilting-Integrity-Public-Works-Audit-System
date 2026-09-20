import React from 'react';
import { EpistemicCategory, TechnicalState } from '@/types/epistemic';
import { EPISTEMIC_CONFIG, TECHNICAL_STATE_CONFIG } from '@/lib/epistemic';
import { cn } from '@/lib/utils';
import { 
  Database, 
  Cpu, 
  Scale, 
  Network, 
  CheckCircle2, 
  HelpCircle, 
  FileQuestion, 
  ShieldAlert, 
  XCircle, 
  RefreshCw, 
  AlertCircle 
} from 'lucide-react';

const ICON_MAP = {
  Database,
  Cpu,
  Scale,
  Network,
  CheckCircle2,
  HelpCircle,
  FileQuestion,
  ShieldAlert,
  XCircle,
  RefreshCw,
  AlertCircle,
};

interface EpistemicBadgeProps {
  category?: EpistemicCategory;
  technicalState?: TechnicalState;
  className?: string;
  showDescription?: boolean;
}

/**
 * EpistemicBadge ensures adherence to the core MuniAudit-AI rule:
 * Epistemic states and technical states MUST NEVER be encoded by color alone.
 * Always renders icon + text alongside color styling.
 */
export const EpistemicBadge: React.FC<EpistemicBadgeProps> = ({
  category,
  technicalState,
  className,
  showDescription = false,
}) => {
  if (!category && !technicalState) return null;

  const config = category 
    ? EPISTEMIC_CONFIG[category] 
    : TECHNICAL_STATE_CONFIG[technicalState!];

  if (!config) return null;

  const IconComponent = ICON_MAP[config.iconName as keyof typeof ICON_MAP] || HelpCircle;

  return (
    <div className={cn("inline-flex flex-col gap-0.5", className)}>
      <span
        className={cn(
          "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-xs font-mono font-medium border shadow-xs tracking-wider",
          config.badgeClass
        )}
        title={config.description}
        data-testid={`epistemic-badge-${category || technicalState}`}
      >
        <IconComponent className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
        <span>{config.label}</span>
      </span>
      {showDescription && (
        <span className="text-[11px] text-slate-400 font-sans leading-tight">
          {config.description}
        </span>
      )}
    </div>
  );
};
