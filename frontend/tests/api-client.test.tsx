import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { AuditApiClient } from '@/lib/api/client';

describe('Canonical Frozen Alpha API Client', () => {
  let client: AuditApiClient;

  beforeEach(() => {
    client = new AuditApiClient('http://localhost:8000');
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('calls GET /health when checking connectivity', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'healthy' }),
    } as any);

    const isHealthy = await client.checkHealth();
    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/health',
      expect.objectContaining({ method: 'GET', signal: expect.any(Object) })
    );
    expect(isHealthy).toBe(true);
    expect(client.getConnectionState()).toBe('LIVE_BACKEND');
  });

  it('returns benchmark dossiers when listing dossiers without calling nonexistent route', async () => {
    global.fetch = vi.fn();
    const result = await client.listDossiers();
    expect(global.fetch).not.toHaveBeenCalled();
    expect(result.length).toBeGreaterThan(0);
  });

  it('calls GET /dossiers/{id} when retrieving a dossier', async () => {
    const mockDossier = { id: 'DOS-001', claimNumber: 'RA-01' };
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockDossier,
    } as any);

    const result = await client.getDossier('DOS-001');
    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/dossiers/DOS-001',
      expect.objectContaining({ signal: expect.any(Object) })
    );
    expect(result).toEqual(mockDossier);
  });

  it('calls GET /dossiers/{id}/triage', async () => {
    const mockTriage = { id: 'DOS-001', claimNumber: 'RA-01', arpiScore: 80 };
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockTriage,
    } as any);

    const result = await client.getDossierTriage('DOS-001');
    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/dossiers/DOS-001/triage',
      expect.objectContaining({ signal: expect.any(Object) })
    );
    expect(result).toEqual(mockTriage);
  });

  it('calls POST /dossiers/{id}/audit', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ success: true, dossierId: 'DOS-001', status: 'AUDIT_COMPLETED' }),
    } as any);

    const result = await client.triggerAudit('DOS-001');
    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/dossiers/DOS-001/audit',
      expect.objectContaining({ method: 'POST' })
    );
    expect(result.success).toBe(true);
  });

  it('calls GET /dossiers/{id}/visual-package', async () => {
    const mockEvidence = [{ id: 'EV-01', type: 'SITE_PHOTO' }];
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockEvidence,
    } as any);

    const result = await client.getVisualPackage('DOS-001');
    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/dossiers/DOS-001/visual-package',
      expect.objectContaining({ signal: expect.any(Object) })
    );
    expect(result).toEqual(mockEvidence);
  });

  it('calls GET /dossiers/{id}/findings', async () => {
    const mockFindings = [{ id: 'FND-01', title: 'Test Finding' }];
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockFindings,
    } as any);

    const result = await client.getFindings('DOS-001');
    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/dossiers/DOS-001/findings',
      expect.objectContaining({ signal: expect.any(Object) })
    );
    expect(result).toEqual(mockFindings);
  });

  it('calls POST /findings/{id}/review', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ success: true, findingId: 'FND-01', action: 'CONCUR', reviewerId: 'OFFICER-01' }),
    } as any);

    const result = await client.submitReview('FND-01', {
      action: 'CONCUR',
      notes: 'Verified against primary evidence.',
      reviewerId: 'OFFICER-01',
      signedAt: '2026-03-20T12:00:00Z',
      evidenceVerifiedAcknowledgement: true,
    });

    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/findings/FND-01/review',
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
    );
    expect(result.success).toBe(true);
  });

  it('falls back to offline fixture state when health check fails', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('Connection refused'));

    const isHealthy = await client.checkHealth();
    expect(isHealthy).toBe(false);
    expect(client.getConnectionState()).toBe('OFFLINE_FIXTURE');
  });
});
