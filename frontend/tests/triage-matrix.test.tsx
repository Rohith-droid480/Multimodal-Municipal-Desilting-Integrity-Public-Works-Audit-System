import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { TriageMatrix } from '@/components/triage/triage-matrix';
import { BENCHMARK_DOSSIER_LIST } from '@/lib/api/fixtures';

describe('Executive Case Triage Matrix Component', () => {
  it('renders all 3 benchmark dossiers with correct case types and tiers', () => {
    render(
      <TriageMatrix
        dossiers={BENCHMARK_DOSSIER_LIST}
        connectionState="OFFLINE_FIXTURE"
        onOpenDossier={vi.fn()}
        onTriggerAudit={vi.fn()}
        onExportJson={vi.fn()}
        onExportMarkdown={vi.fn()}
      />
    );

    expect(screen.getByText('Executive Case Triage Matrix')).toBeInTheDocument();
    expect(screen.getByText('DOSSIER-BLR-2026-W09-042')).toBeInTheDocument();
    expect(screen.getByText('DOSSIER-BLR-2026-W14-018')).toBeInTheDocument();
    expect(screen.getByText('DOSSIER-BLR-2026-W22-099')).toBeInTheDocument();

    expect(screen.getByText('SUBSTANTIVE_INCONSISTENCY')).toBeInTheDocument();
    expect(screen.getByText('CLEAN_COMPLIANT')).toBeInTheDocument();
    expect(screen.getByText('INCONCLUSIVE_DATA')).toBeInTheDocument();

    expect(screen.getByText(/DEMO_FIXTURE \(OFFLINE BENCHMARK\)/i)).toBeInTheDocument();
  });

  it('filters dossiers by search term', () => {
    render(
      <TriageMatrix
        dossiers={BENCHMARK_DOSSIER_LIST}
        connectionState="OFFLINE_FIXTURE"
        onOpenDossier={vi.fn()}
        onTriggerAudit={vi.fn()}
        onExportJson={vi.fn()}
        onExportMarkdown={vi.fn()}
      />
    );

    const searchInput = screen.getByTestId('triage-search-input');
    fireEvent.change(searchInput, { target: { value: 'Yelahanka' } });

    expect(screen.getByText('DOSSIER-BLR-2026-W14-018')).toBeInTheDocument();
    expect(screen.queryByText('DOSSIER-BLR-2026-W09-042')).not.toBeInTheDocument();
    expect(screen.queryByText('DOSSIER-BLR-2026-W22-099')).not.toBeInTheDocument();
  });

  it('filters dossiers by benchmark case selector', () => {
    render(
      <TriageMatrix
        dossiers={BENCHMARK_DOSSIER_LIST}
        connectionState="OFFLINE_FIXTURE"
        onOpenDossier={vi.fn()}
        onTriggerAudit={vi.fn()}
        onExportJson={vi.fn()}
        onExportMarkdown={vi.fn()}
      />
    );

    const filterCase = screen.getByTestId('triage-filter-case');
    fireEvent.change(filterCase, { target: { value: 'INCONCLUSIVE_DATA' } });

    expect(screen.getByText('DOSSIER-BLR-2026-W22-099')).toBeInTheDocument();
    expect(screen.queryByText('DOSSIER-BLR-2026-W09-042')).not.toBeInTheDocument();
    expect(screen.queryByText('DOSSIER-BLR-2026-W14-018')).not.toBeInTheDocument();
  });

  it('triggers onOpenDossier when clicking Workspace button', () => {
    const handleOpen = vi.fn();
    render(
      <TriageMatrix
        dossiers={BENCHMARK_DOSSIER_LIST}
        connectionState="OFFLINE_FIXTURE"
        onOpenDossier={handleOpen}
        onTriggerAudit={vi.fn()}
        onExportJson={vi.fn()}
        onExportMarkdown={vi.fn()}
      />
    );

    const openBtn = screen.getByTestId('open-workspace-btn-DOSSIER-BLR-2026-W09-042');
    fireEvent.click(openBtn);
    expect(handleOpen).toHaveBeenCalledWith('DOSSIER-BLR-2026-W09-042');
  });

  it('triggers onExportJson when clicking JSON button', () => {
    const handleExportJson = vi.fn();
    render(
      <TriageMatrix
        dossiers={BENCHMARK_DOSSIER_LIST}
        connectionState="OFFLINE_FIXTURE"
        onOpenDossier={vi.fn()}
        onExportJson={handleExportJson}
        onExportMarkdown={vi.fn()}
      />
    );

    const jsonBtn = screen.getByTestId('export-json-btn-DOSSIER-BLR-2026-W09-042');
    fireEvent.click(jsonBtn);
    expect(handleExportJson).toHaveBeenCalledWith('DOSSIER-BLR-2026-W09-042');
  });
});
