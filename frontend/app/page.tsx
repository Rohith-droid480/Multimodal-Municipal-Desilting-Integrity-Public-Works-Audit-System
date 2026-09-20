'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { DossierSummary, DossierListItem } from '@/types/dossier';
import { EvidenceItem } from '@/types/evidence';
import { Finding } from '@/types/finding';
import { ReviewAction } from '@/types/review';
import { apiClient, BackendConnectionState } from '@/lib/api/client';
import { TriageMatrix } from '@/components/triage/triage-matrix';
import { Topbar } from '@/components/workspace/topbar';
import { EvidenceTree } from '@/components/workspace/evidence-tree';
import { EvidenceCanvas } from '@/components/workspace/evidence-canvas';
import { FindingRail } from '@/components/workspace/finding-rail';
import { StatusBar } from '@/components/workspace/status-bar';
import { LoadingState, EmptyState } from '@/components/workspace/state-views';

export default function AuditorConsolePage() {
  // Navigation & View State
  const [activeDossierId, setActiveDossierId] = useState<string | null>(null);
  const [connectionState, setConnectionState] = useState<BackendConnectionState>('OFFLINE_FIXTURE');

  // Data State
  const [dossierList, setDossierList] = useState<DossierListItem[]>([]);
  const [activeDossier, setActiveDossier] = useState<DossierSummary | null>(null);
  const [evidenceList, setEvidenceList] = useState<EvidenceItem[]>([]);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string | null>(null);
  const [selectedFindingId, setSelectedFindingId] = useState<string | null>(null);

  // Status States
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [loadingStep, setLoadingStep] = useState<string>('Connecting to MuniAudit-AI Console...');

  // Initialize: Check backend and load triage dossier list
  useEffect(() => {
    async function initConsole() {
      setIsLoading(true);
      setLoadingStep('Checking backend connectivity (http://localhost:8000)...');
      try {
        await apiClient.checkHealth();
        setConnectionState(apiClient.getConnectionState());

        setLoadingStep('Loading executive triage matrix dossiers...');
        const list = await apiClient.listDossiers();
        setDossierList(list);
      } catch (err) {
        console.warn('[AuditorConsole] Initialization warning, using benchmark fallback:', err);
      } finally {
        setIsLoading(false);
      }
    }

    initConsole();
  }, []);

  // Load a specific dossier into Forensic Workspace
  const handleOpenDossier = useCallback(async (dossierId: string) => {
    setIsLoading(true);
    setLoadingStep(`Ingesting dossier ${dossierId} artifacts and initializing forensic workspace...`);
    setActiveDossierId(dossierId);

    try {
      const [dossierData, visualPackage, findingsData] = await Promise.all([
        apiClient.getDossierTriage(dossierId),
        apiClient.getVisualPackage(dossierId),
        apiClient.getFindings(dossierId),
      ]);

      setActiveDossier(dossierData);
      setEvidenceList(visualPackage);
      setFindings(findingsData);

      if (visualPackage.length > 0) {
        setSelectedEvidenceId(visualPackage[0].id);
      } else {
        setSelectedEvidenceId(null);
      }

      if (findingsData.length > 0) {
        setSelectedFindingId(findingsData[0].id);
      } else {
        setSelectedFindingId(null);
      }
    } catch (err) {
      console.error('[AuditorConsole] Error loading dossier:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Return to Triage Matrix
  const handleBackToTriage = () => {
    setActiveDossierId(null);
    setActiveDossier(null);
    setEvidenceList([]);
    setFindings([]);
    setSelectedEvidenceId(null);
    setSelectedFindingId(null);
  };

  // Trigger audit on a dossier (POST /dossiers/{id}/audit)
  const handleTriggerAudit = async (dossierId: string) => {
    await apiClient.triggerAudit(dossierId);
    // Refresh list
    const updatedList = await apiClient.listDossiers();
    setDossierList(updatedList);
  };

  // Export JSON Workpaper (GET /dossiers/{id}/export/json)
  const handleExportJson = async (dossierId: string) => {
    const jsonStr = await apiClient.exportJson(dossierId);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `GAGAS_Workpaper_${dossierId}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Export Markdown Workpaper (GET /dossiers/{id}/export/markdown)
  const handleExportMarkdown = async (dossierId: string) => {
    const mdStr = await apiClient.exportMarkdown(dossierId);
    const blob = new Blob([mdStr], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `GAGAS_Workpaper_${dossierId}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Link finding selection to source evidence in the canvas
  const handleSelectFinding = (findingId: string) => {
    setSelectedFindingId(findingId);
    const finding = findings.find((f) => f.id === findingId);
    if (finding && finding.causality.evidenceIds.length > 0) {
      setSelectedEvidenceId(finding.causality.evidenceIds[0]);
    }
  };

  // Cognitive Review Gate Adjudication (POST /findings/{id}/review)
  const handleAdjudicate = async (
    findingId: string, 
    action: ReviewAction, 
    notes: string, 
    justification?: string
  ) => {
    const response = await apiClient.submitReview(findingId, {
      action,
      notes,
      reviewerId: 'OFFICER-AUDIT-084',
      signedAt: new Date().toISOString(),
      evidenceVerifiedAcknowledgement: true,
      justification,
    });

    // Update local state to reflect adjudication
    setFindings((prev) =>
      prev.map((f) =>
        f.id === findingId
          ? {
              ...f,
              reviewedBy: response.reviewerId,
              reviewedAt: response.recordedAt,
              reviewAction: response.action,
              reviewerNotes: notes,
              overrideJustification: justification,
            }
          : f
      )
    );
  };

  if (isLoading) {
    return <LoadingState step={loadingStep} />;
  }

  // VIEW 1: Executive Case Triage Matrix
  if (!activeDossierId || !activeDossier) {
    return (
      <TriageMatrix
        dossiers={dossierList}
        connectionState={connectionState}
        onOpenDossier={handleOpenDossier}
        onTriggerAudit={handleTriggerAudit}
        onExportJson={handleExportJson}
        onExportMarkdown={handleExportMarkdown}
      />
    );
  }

  // VIEW 2: Forensic Workspace
  const selectedEvidence = evidenceList.find((e) => e.id === selectedEvidenceId) || null;

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-app-bg text-slate-100">
      {/* 1. Header / Engagement Bar with Back button and Export triggers */}
      <Topbar 
        dossier={activeDossier} 
        connectionState={connectionState}
        onBackToTriage={handleBackToTriage}
        onExportJson={handleExportJson}
        onExportMarkdown={handleExportMarkdown}
      />

      {/* 2. Synchronized 3-Column Forensic Workspace */}
      <div className="flex flex-1 min-h-0 overflow-hidden">
        {/* Column 1: Evidence Hierarchy Tree */}
        <EvidenceTree
          evidenceList={evidenceList}
          selectedId={selectedEvidenceId}
          onSelect={(id) => setSelectedEvidenceId(id)}
        />

        {/* Column 2: Contextual Evidence Canvas (Document / Visual / GIS modes) */}
        <EvidenceCanvas selectedItem={selectedEvidence} />

        {/* Column 3: Finding & Causality Inspector (5 GAGAS elements & Cognitive Review Gate) */}
        <FindingRail
          findings={findings}
          selectedFindingId={selectedFindingId}
          onSelectFinding={handleSelectFinding}
          onAdjudicate={handleAdjudicate}
        />
      </div>

      {/* 3. Bottom Status & Provenance Bar */}
      <StatusBar dossier={activeDossier} connectionState={connectionState} />
    </div>
  );
}
