import React, { useState } from 'react';
import { DossierListItem, BenchmarkCase, PriorityTier } from '@/types/dossier';
import { formatCurrencyINR, formatPercentage } from '@/lib/utils';
import { AUDIT_STATUS_CONFIG } from '@/lib/epistemic';
import { 
  Shield, 
  Search, 
  Filter, 
  ArrowRight, 
  Download, 
  AlertTriangle, 
  CheckCircle2, 
  HelpCircle,
  FileSpreadsheet,
  Building2,
  MapPin,
  Server
} from 'lucide-react';

interface TriageMatrixProps {
  dossiers: DossierListItem[];
  connectionState: 'LIVE_BACKEND' | 'OFFLINE_FIXTURE';
  onOpenDossier: (dossierId: string) => void;
  onTriggerAudit?: (dossierId: string) => Promise<void>;
  onExportJson: (dossierId: string) => void;
  onExportMarkdown: (dossierId: string) => void;
}

export const TriageMatrix: React.FC<TriageMatrixProps> = ({
  dossiers,
  connectionState,
  onOpenDossier,
  onTriggerAudit,
  onExportJson,
  onExportMarkdown,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCase, setFilterCase] = useState<string>('ALL');
  const [filterTier, setFilterTier] = useState<string>('ALL');

  // Filter logic
  const filtered = dossiers.filter((d) => {
    const matchesSearch = 
      d.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.workOrderNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.contractorName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.wardNumber.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesCase = filterCase === 'ALL' || d.benchmarkCase === filterCase;
    const matchesTier = filterTier === 'ALL' || d.priorityTier === filterTier;

    return matchesSearch && matchesCase && matchesTier;
  });

  const totalExposure = dossiers.reduce((acc, d) => acc + d.financialExposureInr, 0);
  const avgArpi = Math.round(dossiers.reduce((acc, d) => acc + d.arpiScore, 0) / (dossiers.length || 1));
  const avgEcs = dossiers.reduce((acc, d) => acc + d.ecsScore, 0) / (dossiers.length || 1);

  return (
    <div className="flex-1 flex flex-col bg-app-bg text-slate-100 overflow-y-auto">
      {/* Top Header & Triage Summary Banner */}
      <div className="bg-app-surface border-b border-app-border p-6 shrink-0">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-xs font-mono font-bold bg-sky-950 text-sky-300 border border-sky-800 px-2.5 py-0.5 rounded">
                MuniAudit-AI Console
              </span>
              <span className="text-xs font-mono text-slate-400">
                Milestone 11 Forensic Triage
              </span>
              {connectionState === 'LIVE_BACKEND' ? (
                <span className="inline-flex items-center gap-1 text-xs font-mono bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded">
                  <Server className="w-3 h-3 text-emerald-400" />
                  LIVE_BACKEND (commit: 727b9e3)
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 text-xs font-mono bg-amber-950/80 text-amber-300 border border-amber-800 px-2 py-0.5 rounded">
                  <AlertTriangle className="w-3 h-3 text-amber-400" />
                  DEMO_FIXTURE (OFFLINE BENCHMARK)
                </span>
              )}
            </div>
            <h1 className="text-xl font-bold text-slate-100 mt-2">
              Executive Case Triage Matrix
            </h1>
            <p className="text-xs text-slate-400 mt-0.5 max-w-2xl">
              Triage public-works desilting claims by Audit Review Priority Index (ARPI) and Evidence Consistency Score (ECS). Prioritize high-risk claims for forensic inspection.
            </p>
          </div>

          {/* Aggregate KPI Summary Cards */}
          <div className="grid grid-cols-3 gap-3 shrink-0">
            <div className="bg-app-elevated p-3 rounded-lg border border-app-border min-w-36">
              <div className="text-[11px] font-mono text-slate-400 uppercase">
                Total Exposure
              </div>
              <div className="text-base font-mono font-bold text-slate-100 mt-0.5">
                {formatCurrencyINR(totalExposure)}
              </div>
            </div>

            <div className="bg-app-elevated p-3 rounded-lg border border-app-border min-w-32">
              <div className="text-[11px] font-mono text-slate-400 uppercase">
                Avg ARPI Priority
              </div>
              <div className="text-base font-mono font-bold text-orange-400 mt-0.5">
                {avgArpi} / 100
              </div>
            </div>

            <div className="bg-app-elevated p-3 rounded-lg border border-app-border min-w-32">
              <div className="text-[11px] font-mono text-slate-400 uppercase">
                Avg ECS Coherence
              </div>
              <div className="text-base font-mono font-bold text-sky-400 mt-0.5">
                {formatPercentage(avgEcs)}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 px-6 bg-app-surface/60 border-b border-app-border flex items-center justify-between flex-wrap gap-3 shrink-0">
        <div className="flex items-center gap-3 flex-1 min-w-72 max-w-md">
          <div className="relative w-full">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by Dossier ID, Work Order, Ward, or Contractor..."
              className="w-full bg-app-elevated border border-app-border rounded-md pl-9 pr-3 py-1.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-hidden focus:border-sky-500 font-sans"
              data-testid="triage-search-input"
            />
          </div>
        </div>

        <div className="flex items-center gap-2 flex-wrap text-xs font-mono">
          {/* Benchmark Case Filter */}
          <div className="flex items-center gap-1.5 bg-app-elevated border border-app-border rounded-md px-2.5 py-1">
            <span className="text-slate-400">Case:</span>
            <select
              value={filterCase}
              onChange={(e) => setFilterCase(e.target.value)}
              className="bg-transparent text-slate-200 focus:outline-hidden cursor-pointer"
              data-testid="triage-filter-case"
            >
              <option value="ALL" className="bg-slate-900">All Benchmark Cases</option>
              <option value="SUBSTANTIVE_INCONSISTENCY" className="bg-slate-900">Substantive Inconsistency</option>
              <option value="CLEAN_COMPLIANT" className="bg-slate-900">Clean Compliant</option>
              <option value="INCONCLUSIVE_DATA" className="bg-slate-900">Inconclusive Data</option>
            </select>
          </div>

          {/* Priority Tier Filter */}
          <div className="flex items-center gap-1.5 bg-app-elevated border border-app-border rounded-md px-2.5 py-1">
            <span className="text-slate-400">Tier:</span>
            <select
              value={filterTier}
              onChange={(e) => setFilterTier(e.target.value)}
              className="bg-transparent text-slate-200 focus:outline-hidden cursor-pointer"
              data-testid="triage-filter-tier"
            >
              <option value="ALL" className="bg-slate-900">All Priority Tiers</option>
              <option value="P1_CRITICAL" className="bg-slate-900">P1 Critical</option>
              <option value="P2_HIGH" className="bg-slate-900">P2 High</option>
              <option value="P3_ELEVATED" className="bg-slate-900">P3 Elevated</option>
              <option value="P4_ROUTINE" className="bg-slate-900">P4 Routine</option>
            </select>
          </div>
        </div>
      </div>

      {/* Triage Matrix Table */}
      <div className="flex-1 p-6 overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs" data-testid="triage-table">
          <thead>
            <tr className="border-b border-app-border text-slate-400 font-mono text-[11px] uppercase tracking-wider">
              <th className="pb-3 font-semibold">Dossier ID / Claim</th>
              <th className="pb-3 font-semibold">Ward & Work Order</th>
              <th className="pb-3 font-semibold">Contractor</th>
              <th className="pb-3 font-semibold text-right">Exposure (INR)</th>
              <th className="pb-3 font-semibold text-center">ARPI Priority</th>
              <th className="pb-3 font-semibold text-center">ECS Coherence</th>
              <th className="pb-3 font-semibold text-center">Admin State</th>
              <th className="pb-3 font-semibold text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-app-border font-sans">
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={8} className="py-8 text-center text-slate-500 font-mono">
                  No dossiers match the selected search or filter criteria.
                </td>
              </tr>
            ) : (
              filtered.map((d) => {
                const statusCfg = AUDIT_STATUS_CONFIG[d.status];

                let tierColor = 'bg-slate-800 text-slate-300 border-slate-700';
                if (d.priorityTier === 'P1_CRITICAL') tierColor = 'bg-red-950 text-red-300 border-red-800';
                else if (d.priorityTier === 'P2_HIGH') tierColor = 'bg-orange-950 text-orange-300 border-orange-800';
                else if (d.priorityTier === 'P3_ELEVATED') tierColor = 'bg-amber-950 text-amber-300 border-amber-800';
                else if (d.priorityTier === 'P4_ROUTINE') tierColor = 'bg-emerald-950 text-emerald-300 border-emerald-800';

                return (
                  <tr 
                    key={d.id} 
                    className="hover:bg-app-elevated/50 transition-colors"
                    data-testid={`triage-row-${d.id}`}
                  >
                    {/* Dossier ID & Benchmark Tag */}
                    <td className="py-3.5 pr-4">
                      <div className="font-mono font-semibold text-slate-100 flex items-center gap-1.5">
                        <button
                          onClick={() => onOpenDossier(d.id)}
                          className="hover:text-sky-400 transition-colors text-left"
                          title="Open Forensic Workspace"
                        >
                          {d.id}
                        </button>
                      </div>
                      <div className="text-[11px] font-mono text-slate-400 mt-0.5">
                        {d.claimNumber}
                      </div>
                      <span className="inline-block text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800/80 text-slate-400 border border-slate-700 mt-1">
                        {d.benchmarkCase}
                      </span>
                    </td>

                    {/* Ward & Work Order */}
                    <td className="py-3.5 pr-4 text-slate-300">
                      <div className="font-medium flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-slate-500" />
                        {d.wardNumber}
                      </div>
                      <div className="text-[11px] text-slate-500 font-mono mt-0.5 flex items-center gap-1">
                        <FileSpreadsheet className="w-3 h-3" />
                        WO: {d.workOrderNumber}
                      </div>
                    </td>

                    {/* Contractor */}
                    <td className="py-3.5 pr-4 text-slate-300 max-w-xs truncate">
                      <div className="font-medium truncate">{d.contractorName}</div>
                      <div className="text-[11px] text-slate-500 font-mono mt-0.5">
                        Submitted: {new Date(d.submittedAt).toLocaleDateString('en-IN')}
                      </div>
                    </td>

                    {/* Financial Exposure */}
                    <td className="py-3.5 pr-4 text-right font-mono font-bold text-slate-100">
                      {formatCurrencyINR(d.financialExposureInr)}
                    </td>

                    {/* ARPI Priority */}
                    <td className="py-3.5 pr-4 text-center">
                      <div className="font-mono font-bold text-orange-400 text-sm">
                        {d.arpiScore} / 100
                      </div>
                      <span className={`inline-block text-[10px] font-mono px-1.5 py-0.2 rounded border mt-0.5 ${tierColor}`}>
                        {d.priorityTier}
                      </span>
                    </td>

                    {/* ECS Coherence */}
                    <td className="py-3.5 pr-4 text-center">
                      <div className={`font-mono font-bold text-sm ${d.ecsScore > 0.7 ? 'text-emerald-400' : d.ecsScore > 0.4 ? 'text-amber-400' : 'text-red-400'}`}>
                        {formatPercentage(d.ecsScore)}
                      </div>
                      <div className="w-16 bg-slate-800 h-1.5 rounded-full mx-auto mt-1 overflow-hidden">
                        <div 
                          className={`h-full ${d.ecsScore > 0.7 ? 'bg-emerald-500' : d.ecsScore > 0.4 ? 'bg-amber-500' : 'bg-red-500'}`}
                          style={{ width: `${Math.min(d.ecsScore * 100, 100)}%` }}
                        />
                      </div>
                    </td>

                    {/* Administrative State */}
                    <td className="py-3.5 pr-4 text-center">
                      <span className={`inline-flex items-center gap-1 text-[11px] font-mono px-2 py-0.5 rounded border ${statusCfg.badgeClass}`}>
                        {statusCfg.label}
                      </span>
                    </td>

                    {/* Actions */}
                    <td className="py-3.5 text-right space-x-1.5">
                      <button
                        onClick={() => onExportJson(d.id)}
                        title="Download GAGAS JSON Workpaper"
                        className="p-1.5 bg-app-elevated hover:bg-slate-700 text-slate-300 hover:text-slate-100 rounded border border-app-border transition-colors font-mono text-[11px]"
                        data-testid={`export-json-btn-${d.id}`}
                      >
                        JSON
                      </button>

                      <button
                        onClick={() => onExportMarkdown(d.id)}
                        title="Download GAGAS Markdown Workpaper"
                        className="p-1.5 bg-app-elevated hover:bg-slate-700 text-slate-300 hover:text-slate-100 rounded border border-app-border transition-colors font-mono text-[11px]"
                        data-testid={`export-md-btn-${d.id}`}
                      >
                        MD
                      </button>

                      <button
                        onClick={() => onOpenDossier(d.id)}
                        className="inline-flex items-center gap-1 bg-sky-950 hover:bg-sky-900 text-sky-200 border border-sky-800 py-1 px-2.5 rounded font-mono text-xs font-semibold transition-colors"
                        data-testid={`open-workspace-btn-${d.id}`}
                      >
                        <span>Workspace</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
