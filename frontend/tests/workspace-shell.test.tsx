import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Topbar } from '@/components/workspace/topbar';
import { StatusBar } from '@/components/workspace/status-bar';
import { DEMO_DOSSIER } from '@/lib/api/fixtures';

describe('Auditor Workspace Shell Layout', () => {
  it('renders Topbar with contractor identity and triage scores', () => {
    render(<Topbar dossier={DEMO_DOSSIER} />);
    expect(screen.getByText('Cauvery Infra & Desilting Services Ltd.')).toBeInTheDocument();
    expect(screen.getByText(/RA-BILL\/2026\/03\/42/)).toBeInTheDocument();
    expect(screen.getByText(/ECS Coherence/i)).toBeInTheDocument();
    expect(screen.getByText(/ARPI Priority/i)).toBeInTheDocument();
  });

  it('renders StatusBar with demo mode indicator and pipeline status', () => {
    render(<StatusBar dossier={DEMO_DOSSIER} />);
    expect(screen.getByText(/MODE: DEMO_FIXTURE/i)).toBeInTheDocument();
    expect(screen.getByText(/Pipeline: NORMALIZED & INDEXED/i)).toBeInTheDocument();
  });
});
