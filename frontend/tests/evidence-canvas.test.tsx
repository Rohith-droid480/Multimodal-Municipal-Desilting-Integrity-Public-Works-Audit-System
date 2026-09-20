import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { EvidenceCanvas } from '@/components/workspace/evidence-canvas';
import { BENCHMARK_EVIDENCE } from '@/lib/api/fixtures';

describe('Contextual Evidence Canvas Component', () => {
  const evidenceList = BENCHMARK_EVIDENCE['DOSSIER-BLR-2026-W09-042'];

  it('renders Document Mode with thermal receipt, bounding boxes, and multi-page pagination', () => {
    const receiptItem = evidenceList.find((e) => e.type === 'WEIGHBRIDGE_RECEIPT')!;
    render(<EvidenceCanvas selectedItem={receiptItem} />);

    expect(screen.getByTestId('document-mode-canvas')).toBeInTheDocument();
    expect(screen.getByText('Page 1 of 3')).toBeInTheDocument();
    expect(screen.getByText(/Pages 2, 3: Unprocessed \/ Backend Preservation Gap/i)).toBeInTheDocument();
    expect(screen.getByTestId('bbox-gross_weight')).toBeInTheDocument();
    expect(screen.getByTestId('bbox-tare_weight')).toBeInTheDocument();
  });

  it('renders Visual Forensics Mode with SSCD similarity and RANSAC inliers', () => {
    const photoItem = evidenceList.find((e) => e.id === 'EV-PHOTO-002')!;
    render(<EvidenceCanvas selectedItem={photoItem} />);

    expect(screen.getByTestId('visual-mode-canvas')).toBeInTheDocument();
    expect(screen.getByText(/SSCD Similarity:/i)).toBeInTheDocument();
    expect(screen.getByText('96.4%')).toBeInTheDocument();
    expect(screen.getByText(/42 keypoints/i)).toBeInTheDocument();
    expect(screen.getByText('Current Claim Photo (EV-PHOTO-002)')).toBeInTheDocument();
    expect(screen.getByText(/Historical Match/i)).toBeInTheDocument();
  });

  it('renders GIS Telemetry Mode with drain centerline and transit velocity', () => {
    const tripItem = evidenceList.find((e) => e.type === 'VEHICLE_TRIP')!;
    render(<EvidenceCanvas selectedItem={tripItem} />);

    expect(screen.getByTestId('gis-mode-canvas')).toBeInTheDocument();
    expect(screen.getByText(/PostGIS Spatial Verification Canvas/i)).toBeInTheDocument();
    expect(screen.getByText('SWD-BLR-NZ-09-02')).toBeInTheDocument();
    expect(screen.getByText(/Stationing: Ch 1200m to 2400m/i)).toBeInTheDocument();
    expect(screen.getByText(/Mavallipura Landfill/i)).toBeInTheDocument();
    expect(screen.getByText(/11.4 km/i)).toBeInTheDocument();
    expect(screen.getByText(/18 km\/h/i)).toBeInTheDocument();
  });
});
