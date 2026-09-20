import React from 'react';
import { SeverityLevel } from '@/types/epistemic';
import { SEVERITY_CONFIG } from '@/lib/epistemic';
import { cn } from '@/lib/utils';
import { 
  AlertOctagon, 
  AlertTriangle, 
  AlertCircle, 
  HelpCircle, 
  ShieldCheck 
} from 'lucide-react';

const ICON_MAP = {
  AlertOctagon,
  AlertTriangle,
  AlertCircle,
  HelpCircle,
  ShieldCheck,
};

interface SeverityBadgeProps {
  severity: SeverityLevel;
  className?: string;
  showIcon?: boolean;
}

/**
 * SeverityBadge enforces dual encoding: color + icon + text.
 * Never allows color to be the sole carrier of severity signal.
 */
export const SeverityBadge: React.FC<SeverityBadgeProps> = ({
  severity,
  className,
  showIcon = true,
}) => {
  const config = SEVERITY_CONFIG[severity];
  if (!config) return null;

  const IconComponent = ICON_MAP[config.iconName as keyof typeof ICON_MAP] || HelpCircle;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-mono font-semibold border shadow-xs tracking-wide",
        config.badgeClass,
        className
      )}
      title={config.description}
      data-testid={`severity-badge-${severity}`}
    >
      {showIcon && <IconComponent className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />}
      <span>{config.label}</span>
    </span>
  );
};
