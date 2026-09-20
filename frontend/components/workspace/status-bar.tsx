import React from 'react';
import { DossierSummary } from '@/types/dossier';
import { Database, GitCommit, ShieldCheck, Server, AlertTriangle } from 'lucide-react';

interface StatusBarProps {
  dossier: DossierSummary;
  connectionState?: 'LIVE_BACKEND' | 'OFFLINE_FIXTURE';
}

export const StatusBar: React.FC<StatusBarProps> = ({ 
  dossier,
  connectionState = 'OFFLINE_FIXTURE',
}) => {
  return (
    <footer className="bg-app-surface border-t border-app-border text-slate-400 px-4 py-1.5 text-xs font-mono flex items-center justify-between shrink-0 select-none flex-wrap gap-2" data-testid="status-bar">
      <div className="flex items-center gap-4 flex-wrap">
        <span className="flex items-center gap-1 text-slate-300">
          <Database className="w-3 h-3 text-sky-400" />
          <span>Dossier: {dossier.id}</span>
        </span>
        <span className="flex items-center gap-1 text-emerald-400">
          <ShieldCheck className="w-3 h-3" />
          <span>Pipeline: NORMALIZED & INDEXED</span>
        </span>
        <span className="text-slate-500">
          Evidence: {dossier.evidenceCounts.photos} Photos, {dossier.evidenceCounts.receipts} Receipts, {dossier.evidenceCounts.trips} Trips
        </span>
        <span className="text-slate-500 text-[11px] hidden lg:inline">
          Epistemic: MODEL_OUTPUT ≠ FACT | UNKNOWN ≠ WRONGDOING
        </span>
      </div>

      <div className="flex items-center gap-3">
        {connectionState === 'LIVE_BACKEND' ? (
          <span className="inline-flex items-center gap-1 text-emerald-400 font-semibold text-[11px]">
            <Server className="w-3 h-3 text-emerald-400" />
            [BACKEND: LIVE (727b9e3)]
          </span>
        ) : (
          <span className="inline-flex items-center gap-1 text-amber-400/90 font-semibold text-[11px]">
            <AlertTriangle className="w-3 h-3 text-amber-400" />
            [MODE: DEMO_FIXTURE (OFFLINE)]
          </span>
        )}
        <span className="text-slate-500 flex items-center gap-1 text-[11px]">
          <GitCommit className="w-3 h-3" />
          <span>v0.1.0-m11.console</span>
        </span>
      </div>
    </footer>
  );
};
