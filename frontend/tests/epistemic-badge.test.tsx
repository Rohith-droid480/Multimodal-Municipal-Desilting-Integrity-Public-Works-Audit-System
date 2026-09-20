import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { EpistemicBadge } from '@/components/ui/epistemic-badge';
import { SeverityBadge } from '@/components/ui/severity-badge';

describe('EpistemicBadge & Dual Encoding Invariant', () => {
  it('renders FACT badge with text and icon', () => {
    render(<EpistemicBadge category="FACT" />);
    const badge = screen.getByTestId('epistemic-badge-FACT');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveTextContent('FACT');
  });

  it('renders MODEL_OUTPUT badge with text and icon', () => {
    render(<EpistemicBadge category="MODEL_OUTPUT" />);
    const badge = screen.getByTestId('epistemic-badge-MODEL_OUTPUT');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveTextContent('MODEL OUTPUT');
  });

  it('renders RULE_RESULT badge with text and icon', () => {
    render(<EpistemicBadge category="RULE_RESULT" />);
    const badge = screen.getByTestId('epistemic-badge-RULE_RESULT');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveTextContent('RULE RESULT');
  });

  it('renders TECHNICAL_ABSTENTION technical state with text and icon', () => {
    render(<EpistemicBadge technicalState="TECHNICAL_ABSTENTION" />);
    const badge = screen.getByTestId('epistemic-badge-TECHNICAL_ABSTENTION');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveTextContent('TECHNICAL ABSTENTION');
  });

  it('renders INCONCLUSIVE_DATA technical state with text and icon', () => {
    render(<EpistemicBadge technicalState="INCONCLUSIVE_DATA" />);
    const badge = screen.getByTestId('epistemic-badge-INCONCLUSIVE_DATA');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveTextContent('INCONCLUSIVE DATA');
  });
});

describe('SeverityBadge Dual Encoding', () => {
  it('renders CRITICAL severity with icon and label', () => {
    render(<SeverityBadge severity="CRITICAL" />);
    const badge = screen.getByTestId('severity-badge-CRITICAL');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveTextContent('CRITICAL');
  });

  it('renders INCONCLUSIVE severity without indicating guilt', () => {
    render(<SeverityBadge severity="INCONCLUSIVE" />);
    const badge = screen.getByTestId('severity-badge-INCONCLUSIVE');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveTextContent('INCONCLUSIVE');
  });
});
