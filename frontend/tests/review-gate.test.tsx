import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { FindingRail } from '@/components/workspace/finding-rail';
import { BENCHMARK_FINDINGS } from '@/lib/api/fixtures';

describe('Cognitive Review Gate Component', () => {
  const findings = BENCHMARK_FINDINGS['DOSSIER-BLR-2026-W09-042'];

  it('renders 5 GAGAS elements for the active finding', () => {
    render(
      <FindingRail
        findings={findings}
        selectedFindingId={findings[0].id}
        onSelectFinding={vi.fn()}
        onAdjudicate={vi.fn()}
      />
    );

    expect(screen.getByTestId('gagas-elements-box')).toBeInTheDocument();
    expect(screen.getByText(/1\. Criteria/i)).toBeInTheDocument();
    expect(screen.getByText(/2\. Condition/i)).toBeInTheDocument();
    expect(screen.getByText(/3\. Cause Hypothesis/i)).toBeInTheDocument();
    expect(screen.getByText(/4\. Effect/i)).toBeInTheDocument();
    expect(screen.getByText(/5\. Recommendation/i)).toBeInTheDocument();
  });

  it('enforces mandatory evidence verification acknowledgement before enabling submission', () => {
    render(
      <FindingRail
        findings={findings}
        selectedFindingId={findings[0].id}
        onSelectFinding={vi.fn()}
        onAdjudicate={vi.fn()}
      />
    );

    const submitBtn = screen.getByTestId('submit-review-btn');
    expect(submitBtn).toBeDisabled();

    const ackCheckbox = screen.getByTestId('evidence-ack-checkbox');
    fireEvent.click(ackCheckbox);

    expect(submitBtn).not.toBeDisabled();
  });

  it('requires justification when OVERRIDE action is selected', () => {
    render(
      <FindingRail
        findings={findings}
        selectedFindingId={findings[0].id}
        onSelectFinding={vi.fn()}
        onAdjudicate={vi.fn()}
      />
    );

    const ackCheckbox = screen.getByTestId('evidence-ack-checkbox');
    fireEvent.click(ackCheckbox);

    const overrideBtn = screen.getByTestId('action-override-btn');
    fireEvent.click(overrideBtn);

    const submitBtn = screen.getByTestId('submit-review-btn');
    // Disabled because override justification is empty
    expect(submitBtn).toBeDisabled();

    const justificationInput = screen.getByTestId('override-justification-input');
    fireEvent.change(justificationInput, { target: { value: 'Contractor provided certified geotagged RAW camera files confirming unique work.' } });

    expect(submitBtn).not.toBeDisabled();
  });

  it('submits CONCUR adjudication with notes', async () => {
    const handleAdjudicate = vi.fn().mockResolvedValue(undefined);
    render(
      <FindingRail
        findings={findings}
        selectedFindingId={findings[0].id}
        onSelectFinding={vi.fn()}
        onAdjudicate={handleAdjudicate}
      />
    );

    const ackCheckbox = screen.getByTestId('evidence-ack-checkbox');
    fireEvent.click(ackCheckbox);

    const notesInput = screen.getByTestId('review-notes-input');
    fireEvent.change(notesInput, { target: { value: 'Issue show cause notice to contractor.' } });

    const submitBtn = screen.getByTestId('submit-review-btn');
    await act(async () => {
      fireEvent.click(submitBtn);
    });

    expect(handleAdjudicate).toHaveBeenCalledWith(
      findings[0].id,
      'CONCUR',
      'Issue show cause notice to contractor.',
      undefined
    );
  });
});
