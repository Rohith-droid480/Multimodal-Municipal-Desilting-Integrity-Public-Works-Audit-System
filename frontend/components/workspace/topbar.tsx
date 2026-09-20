import React from 'react';
import { DossierSummary } from '@/types/dossier';
import { formatCurrencyINR, formatPercentage } from '@/lib/utils';
import { AUDIT_STATUS_CONFIG } from '@/lib/epistemic';
import { 
  Shield, 
  AlertCircle, 
  Building2, 
  MapPin, 
  FileSpreadsheet, 
  Info,
  ArrowLeft,
  Download,
  Server
} from 'lucide-react';

interface TopbarProps {
  dossier: DossierSummary;
  connectionState?: 'LIVE_BACKEND' | 'OFFLINE_FIXTURE';
  onBackToTriage?: () => void;
  onExportJson?: (dossierId: string) => void;
  onExportMarkdown?: (dossierId: string) => void;
}

export const Topbar: React.FC<TopbarProps> = ({ 
  dossier,
  connectionState = 'OFFLINE_FIXTURE',
  onBackToTriage,
  onExportJson,
  onExportMarkdown,
}) => {
  const statusConfig = AUDIT_STATUS_CONFIG[dossier.status];

  return (
    <header className="bg-app-surface border-b border-app-border text-slate-100 px-6 py-3 shrink-0 select-none">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Left: Back Button & Engagement Identity */}
        <div className="flex items-start gap-4">
          {onBackToTriage && (
            <button
              onClick={onBackToTriage}
              title="Return to Executive Case Triage Matrix"
              className="p-2 bg-app-elevated hover:bg-slate-700 text-slate-300 hover:text-slate-100 rounded-lg border border-app-border transition-colors shrink-0 mt-0.5"
              data-testid="back-to-triage-btn"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
          )}

          <div className="p-2.5 bg-app-elevated rounded-lg border border-app-border shrink-0">
            <Shield className="w-6 h-6 text-sky-400" />
          </div>

          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-xs font-mono font-semibold bg-sky-950/80 text-sky-300 border border-sky-800 px-2 py-0.5 rounded">
                MuniAudit-AI Console
              </span>
              <span className="text-xs font-mono text-slate-400">
                {dossier.claimNumber}
              </span>
              <span className={`inline-flex items-center gap-1 text-xs font-mono px-2 py-0.5 rounded border ${statusConfig.badgeClass}`}>
                {statusConfig.label}
              </span>
              {connectionState === 'LIVE_BACKEND' ? (
                <span className="inline-flex items-center gap-1 text-[10px] font-mono bg-emerald-950 text-emerald-300 border border-emerald-800 px-1.5 py-0.2 rounded">
                  <Server className="w-2.5 h-2.5 text-emerald-400" />
                  LIVE
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 text-[10px] font-mono bg-amber-950/80 text-amber-300 border border-amber-800 px-1.5 py-0.2 rounded">
                  DEMO_FIXTURE
                </span>
              )}
            </div>
            <h1 className="text-base font-semibold text-slate-100 mt-1 flex items-center gap-2">
              <span>{dossier.contractor.contractorName}</span>
              <span className="text-xs font-normal text-slate-400 font-mono">
                ({dossier.contractor.contractNumber})
              </span>
            </h1>
            <div className="flex items-center gap-4 text-xs text-slate-400 mt-0.5 flex-wrap">
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-slate-500" />
                {dossier.contractor.wardNumber}
              </span>
              <span className="flex items-center gap-1">
                <Building2 className="w-3.5 h-3.5 text-slate-500" />
                {dossier.contractor.reachName}
              </span>
              <span className="flex items-center gap-1">
                <FileSpreadsheet className="w-3.5 h-3.5 text-slate-500" />
                WO: {dossier.contractor.workOrderNumber}
              </span>
            </div>
          </div>
        </div>

        {/* Right: Financial Exposure, ECS & ARPI Triage Metrics + Export Buttons */}
        <div className="flex items-center gap-4 shrink-0 flex-wrap">
          <div className="flex items-center gap-5 bg-app-elevated/70 p-2.5 rounded-lg border border-app-border">
            {/* Financial Exposure */}
            <div className="text-right">
              <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                Financial Exposure
              </div>
              <div className="text-sm font-mono font-bold text-slate-100">
                {formatCurrencyINR(dossier.financialExposureInr)}
              </div>
            </div>

            <div className="w-px h-8 bg-slate-700/60" />

            {/* Evidence Consistency Score (ECS) */}
            <div className="text-right">
              <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex items-center gap-1 justify-end">
                <span>ECS Coherence</span>
                <span title="Evidence Consistency Score: internal coherence across evidence artifacts (NOT a fraud probability)">
                  <Info className="w-3 h-3 text-slate-500 hover:text-slate-300" />
                </span>
              </div>
              <div className={`text-sm font-mono font-bold ${dossier.ecsScore > 0.7 ? 'text-emerald-400' : dossier.ecsScore > 0.4 ? 'text-amber-400' : 'text-red-400'}`}>
                {formatPercentage(dossier.ecsScore)}
              </div>
            </div>

            <div className="w-px h-8 bg-slate-700/60" />

            {/* Audit Review Priority Index (ARPI) */}
            <div className="text-right">
              <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex items-center gap-1 justify-end">
                <span>ARPI Priority</span>
                <span title="Audit Review Priority Index: triage workload ranking (0-100) (NOT a legal guilt probability)">
                  <AlertCircle className="w-3 h-3 text-orange-400 hover:text-orange-300" />
                </span>
              </div>
              <div className="text-sm font-mono font-bold text-orange-400">
                {dossier.arpiScore} / 100
              </div>
            </div>
          </div>

          {/* Export Workpaper Actions */}
          <div className="flex items-center gap-1.5 font-mono text-xs">
            {onExportJson && (
              <button
                onClick={() => onExportJson(dossier.id)}
                className="bg-app-elevated hover:bg-slate-700 text-slate-200 border border-app-border py-2 px-2.5 rounded-lg transition-colors flex items-center gap-1"
                title="Download GAGAS JSON Workpaper"
                data-testid="workspace-export-json-btn"
              >
                <Download className="w-3.5 h-3.5 text-sky-400" />
                <span>JSON</span>
              </button>
            )}
            {onExportMarkdown && (
              <button
                onClick={() => onExportMarkdown(dossier.id)}
                className="bg-app-elevated hover:bg-slate-700 text-slate-200 border border-app-border py-2 px-2.5 rounded-lg transition-colors flex items-center gap-1"
                title="Download GAGAS Markdown Workpaper"
                data-testid="workspace-export-md-btn"
              >
                <Download className="w-3.5 h-3.5 text-emerald-400" />
                <span>MD</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
