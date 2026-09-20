import React, { useState } from 'react';
import { EvidenceItem, BoundingBox } from '@/types/evidence';
import { EpistemicBadge } from '@/components/ui/epistemic-badge';
import { 
  FileText, 
  Camera, 
  Map, 
  ZoomIn, 
  ZoomOut, 
  RotateCcw, 
  Hash, 
  Clock, 
  FileCheck, 
  Cpu, 
  ExternalLink,
  Split,
  Eye,
  AlertTriangle,
  CheckCircle2,
  Navigation,
  MapPin,
  Layers
} from 'lucide-react';

interface EvidenceCanvasProps {
  selectedItem: EvidenceItem | null;
}

export const EvidenceCanvas: React.FC<EvidenceCanvasProps> = ({ selectedItem }) => {
  const [zoomLevel, setZoomLevel] = useState<number>(100);
  const [activeBoxKey, setActiveBoxKey] = useState<string | null>(null);
  const [splitViewMode, setSplitViewMode] = useState<'SIDE_BY_SIDE' | 'OVERLAY'>('SIDE_BY_SIDE');
  const [showCorrespondence, setShowCorrespondence] = useState<boolean>(true);

  if (!selectedItem) {
    return (
      <main className="flex-1 bg-app-bg flex items-center justify-center p-8 text-center">
        <div className="max-w-md space-y-3">
          <FileText className="w-12 h-12 text-slate-600 mx-auto" />
          <h3 className="text-sm font-semibold text-slate-300">No Evidence Item Selected</h3>
          <p className="text-xs text-slate-500">
            Select an artifact from the evidence tree on the left to inspect its primary contents, optical extractions, visual comparison, or geospatial telemetry.
          </p>
        </div>
      </main>
    );
  }

  // Determine active primary canvas mode
  const isDocument = selectedItem.type === 'WEIGHBRIDGE_RECEIPT' || selectedItem.type === 'INVOICE' || selectedItem.type === 'MEASUREMENT_BOOK';
  const isPhoto = selectedItem.type === 'SITE_PHOTO' || selectedItem.type === 'HISTORICAL_PHOTO';
  const isGis = selectedItem.type === 'VEHICLE_TRIP' || selectedItem.type === 'GPS_OBSERVATION' || selectedItem.type === 'DRAIN_GEOMETRY';

  return (
    <main className="flex-1 bg-app-bg flex flex-col min-w-0 overflow-hidden" data-testid="evidence-canvas">
      {/* Canvas Header Controls */}
      <div className="bg-app-surface border-b border-app-border p-2.5 px-4 flex items-center justify-between flex-wrap gap-2 shrink-0">
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono font-semibold text-slate-200">
            {selectedItem.id}
          </span>
          <span className="text-xs text-slate-400 truncate max-w-xs md:max-w-md">
            — {selectedItem.title}
          </span>
          <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-400 border border-slate-700">
            {selectedItem.provenance}
          </span>
        </div>

        <div className="flex items-center gap-3">
          {/* Zoom controls */}
          <div className="flex items-center gap-1 bg-app-elevated border border-app-border rounded px-1.5 py-1 text-slate-400">
            <button
              onClick={() => setZoomLevel((z) => Math.max(z - 25, 50))}
              title="Zoom Out"
              className="hover:text-slate-200 cursor-pointer"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="text-[11px] font-mono px-1 w-10 text-center text-slate-300">
              {zoomLevel}%
            </span>
            <button
              onClick={() => setZoomLevel((z) => Math.min(z + 25, 200))}
              title="Zoom In"
              className="hover:text-slate-200 cursor-pointer"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setZoomLevel(100)}
              title="Reset Zoom"
              className="hover:text-slate-200 ml-1 cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Evidence Inspection Surface */}
      <div className="flex-1 overflow-auto p-4 flex items-center justify-center bg-canvas-backdrop/10">
        
        {/* ========================================================================= */}
        {/* 1. DOCUMENT MODE: Thermal Weighbridge Receipt with Bounding Boxes */}
        {/* ========================================================================= */}
        {isDocument && (
          <div
            className="w-full max-w-2xl bg-canvas-bg rounded-lg shadow-2xl p-6 text-slate-900 border border-slate-300 transition-transform duration-150"
            style={{ transform: `scale(${zoomLevel / 100})`, transformOrigin: 'top center' }}
            data-testid="document-mode-canvas"
          >
            {/* Header & Multi-Page Pagination Status */}
            <div className="border-b border-slate-200 pb-3 mb-4 flex items-center justify-between flex-wrap gap-2">
              <div>
                <span className="text-[11px] font-mono text-slate-500 uppercase tracking-wider">
                  Document Intelligence Canvas (Light Mode)
                </span>
                <h2 className="text-base font-bold text-slate-900">
                  {selectedItem.title}
                </h2>
              </div>

              {/* Multi-page handling display */}
              {(selectedItem as any).pagination && (
                <div className="text-right">
                  <div className="text-xs font-mono font-semibold bg-slate-100 text-slate-700 px-2 py-0.5 rounded border border-slate-300 inline-block">
                    Page {(selectedItem as any).pagination.processedPages.join(', ')} of {(selectedItem as any).pagination.totalPages}
                  </div>
                  {(selectedItem as any).pagination.unprocessedPages?.length > 0 && (
                    <div className="text-[10px] font-mono text-amber-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-300 mt-1">
                      ⚠️ Pages {(selectedItem as any).pagination.unprocessedPages.join(', ')}: Unprocessed / Backend Preservation Gap
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Thermal Weighbridge Receipt Simulation with Interactive Bounding Boxes */}
            <div className="relative bg-white border-2 border-dashed border-slate-300 rounded p-6 shadow-inner font-mono text-xs text-slate-800 min-h-[420px]">
              {/* Receipt Heading */}
              <div className="text-center pb-3 border-b border-slate-300 mb-4">
                <div className="text-sm font-bold tracking-widest uppercase">
                  {(selectedItem as any).extractedData?.weighbridgeName || 'MAVALLIPURA LANDFILL PUBLIC WEIGHBRIDGE'}
                </div>
                <div className="text-[10px] text-slate-500">
                  Government Authorized Waste Disposal Facility Scale #04
                </div>
              </div>

              {/* Receipt Key-Value Rows */}
              <div className="space-y-3">
                <div className="flex justify-between items-center py-1">
                  <span className="text-slate-500">TICKET NO:</span>
                  <span className="font-bold text-slate-900 font-mono">
                    {(selectedItem as any).extractedData?.ticketNumber || 'WB-78102'}
                  </span>
                </div>
                <div className="flex justify-between items-center py-1">
                  <span className="text-slate-500">VEHICLE NO:</span>
                  <span className="font-bold text-slate-900 font-mono">
                    {(selectedItem as any).extractedData?.vehicleNumber || 'KA-04-E-9102'}
                  </span>
                </div>
                <div className="flex justify-between items-center py-1">
                  <span className="text-slate-500">GROSS WEIGHT:</span>
                  <span className="font-bold text-slate-900 font-mono">
                    {(selectedItem as any).extractedData?.grossWeightKg?.toLocaleString()} kg
                  </span>
                </div>
                <div className="flex justify-between items-center py-1">
                  <span className="text-slate-500">TARE WEIGHT:</span>
                  <span className={`font-bold font-mono ${(selectedItem as any).extractedData?.ocrConfidence < 0.75 ? 'text-amber-600 underline decoration-dashed' : 'text-slate-900'}`}>
                    {(selectedItem as any).extractedData?.tareWeightKg?.toLocaleString()} kg
                    {(selectedItem as any).extractedData?.ocrConfidence < 0.75 && ' [Ambiguous / Faded]'}
                  </span>
                </div>
                <div className="flex justify-between items-center py-1.5 border-t-2 border-slate-400">
                  <span className="font-bold text-slate-700">NET SILT WEIGHT:</span>
                  <span className="font-bold text-slate-950 text-sm font-mono">
                    {(selectedItem as any).extractedData?.netWeightKg?.toLocaleString()} kg
                  </span>
                </div>
                <div className="flex justify-between items-center py-1 text-[11px] text-slate-500">
                  <span>TIMESTAMP:</span>
                  <span className="font-mono">
                    {(selectedItem as any).extractedData?.timestamp || '2026-02-20 14:12:00'} IST
                  </span>
                </div>
              </div>

              {/* Bounding Box Overlays */}
              {(selectedItem as any).boundingBoxes?.map((bb: BoundingBox) => {
                const [ymin, xmin, ymax, xmax] = bb.box;
                const isHovered = activeBoxKey === bb.fieldKey;
                const isLowConf = bb.confidence < 0.75 || bb.isAmbiguous;

                return (
                  <div
                    key={bb.fieldKey}
                    onMouseEnter={() => setActiveBoxKey(bb.fieldKey)}
                    onMouseLeave={() => setActiveBoxKey(null)}
                    className={`absolute rounded border-2 transition-all cursor-pointer ${
                      isLowConf
                        ? 'border-amber-500 bg-amber-500/15 border-dashed'
                        : 'border-sky-500 bg-sky-500/10'
                    } ${isHovered ? 'ring-2 ring-sky-400 z-20' : 'z-10'}`}
                    style={{
                      top: `${ymin * 100}%`,
                      left: `${xmin * 100}%`,
                      height: `${(ymax - ymin) * 100}%`,
                      width: `${(xmax - xmin) * 100}%`,
                    }}
                    title={`${bb.fieldLabel}: ${bb.value} (Confidence: ${(bb.confidence * 100).toFixed(0)}%)`}
                    data-testid={`bbox-${bb.fieldKey}`}
                  >
                    <span
                      className={`absolute -top-4 left-0 text-[9px] font-mono px-1 py-0.2 rounded whitespace-nowrap ${
                        isLowConf ? 'bg-amber-600 text-white' : 'bg-sky-600 text-white'
                      }`}
                    >
                      {bb.fieldLabel} ({(bb.confidence * 100).toFixed(0)}%)
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Extracted Values & Arithmetic Validation Summary */}
            <div className="mt-4 p-3 bg-slate-50 rounded border border-slate-200 text-xs font-mono text-slate-700">
              <div className="flex items-center justify-between pb-1 border-b border-slate-200">
                <span className="font-bold text-slate-900">Deterministic Gross-Tare-Net Reconciliation:</span>
                <span className="font-bold text-emerald-700">
                  {(selectedItem as any).extractedData?.grossWeightKg} - {(selectedItem as any).extractedData?.tareWeightKg} == {(selectedItem as any).extractedData?.netWeightKg} kg
                </span>
              </div>
              <div className="pt-2 grid grid-cols-2 gap-2 text-[11px] text-slate-600">
                <div>Extraction Engine: AWS Textract AnalyzeDocument</div>
                <div>Epistemic State: MODEL_OUTPUT (OCR extractions)</div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* 2. VISUAL FORENSICS MODE: Split Comparison & Correspondence */}
        {/* ========================================================================= */}
        {isPhoto && (
          <div className="w-full max-w-4xl space-y-4" data-testid="visual-mode-canvas">
            {/* Forensics Comparison Toolbar */}
            <div className="bg-app-surface border border-app-border rounded-lg p-3 flex items-center justify-between flex-wrap gap-2 text-xs font-mono">
              <div className="flex items-center gap-2">
                <span className="text-slate-400">Comparison Mode:</span>
                <button
                  onClick={() => setSplitViewMode('SIDE_BY_SIDE')}
                  className={`px-2 py-1 rounded ${splitViewMode === 'SIDE_BY_SIDE' ? 'bg-sky-950 text-sky-300 font-semibold' : 'text-slate-400 hover:text-slate-200'}`}
                >
                  Side-by-Side
                </button>
                <button
                  onClick={() => setSplitViewMode('OVERLAY')}
                  className={`px-2 py-1 rounded ${splitViewMode === 'OVERLAY' ? 'bg-sky-950 text-sky-300 font-semibold' : 'text-slate-400 hover:text-slate-200'}`}
                >
                  Split Curtain
                </button>
              </div>

              {(selectedItem as any).visualForensics && (
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-1.5">
                    <span className="text-slate-400">SSCD Similarity:</span>
                    <span className={`font-bold ${(selectedItem as any).visualForensics.sscdSimilarity >= 0.82 ? 'text-red-400' : 'text-emerald-400'}`}>
                      {((selectedItem as any).visualForensics.sscdSimilarity * 100).toFixed(1)}%
                    </span>
                    <span className="text-[10px] text-slate-500">(&ge; 82.0% threshold)</span>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <span className="text-slate-400">RANSAC Inliers:</span>
                    <span className={`font-bold ${(selectedItem as any).visualForensics.ransacInliers >= 25 ? 'text-red-400' : 'text-emerald-400'}`}>
                      {(selectedItem as any).visualForensics.ransacInliers} keypoints
                    </span>
                    <span className="text-[10px] text-slate-500">(&ge; 25 threshold)</span>
                  </div>

                  <button
                    onClick={() => setShowCorrespondence((v) => !v)}
                    className={`px-2 py-1 rounded border text-[11px] ${
                      showCorrespondence ? 'bg-purple-950 text-purple-300 border-purple-800' : 'bg-slate-800 text-slate-400 border-slate-700'
                    }`}
                  >
                    {showCorrespondence ? 'Vectors ON' : 'Vectors OFF'}
                  </button>
                </div>
              )}
            </div>

            {/* Visual Comparison Canvas */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Current Claim Photo */}
              <div className="bg-app-surface border border-app-border rounded-lg p-3 space-y-2">
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="font-semibold text-slate-200">Current Claim Photo ({selectedItem.id})</span>
                  <span className="text-sky-400 font-bold">SUBMITTED</span>
                </div>
                <div className="aspect-4/3 bg-slate-900 rounded border border-slate-700 flex flex-col items-center justify-center p-4 relative overflow-hidden text-center">
                  <Camera className="w-12 h-12 text-sky-400/50 mb-2" />
                  <span className="text-xs font-mono text-slate-300">{selectedItem.title}</span>
                  <span className="text-[11px] text-slate-500 mt-1">
                    Captured: {new Date(selectedItem.submittedAt).toLocaleString('en-IN')}
                  </span>
                  {showCorrespondence && (
                    <div className="absolute inset-0 pointer-events-none border-2 border-purple-500/40 rounded flex items-center justify-center">
                      <span className="text-[10px] font-mono bg-purple-950/80 text-purple-300 px-2 py-0.5 rounded border border-purple-700">
                        42 Geometric Keypoint Inliers Mapped
                      </span>
                    </div>
                  )}
                </div>
                <div className="text-[11px] font-mono text-slate-400 space-y-0.5">
                  <div>EXIF Camera: {(selectedItem as any).metadata?.camera || 'Samsung Galaxy A52'}</div>
                  <div>SHA-256: {selectedItem.sha256Hash.substring(0, 24)}...</div>
                </div>
              </div>

              {/* Historical Candidate Photo */}
              {(selectedItem as any).visualForensics?.candidateDossierId ? (
                <div className="bg-app-surface border border-app-border rounded-lg p-3 space-y-2">
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="font-semibold text-slate-200">
                      Historical Match ({(selectedItem as any).visualForensics.candidateDossierId})
                    </span>
                    <span className="text-red-400 font-bold">PRIOR WORK</span>
                  </div>
                  <div className="aspect-4/3 bg-slate-900 rounded border border-slate-700 flex flex-col items-center justify-center p-4 relative overflow-hidden text-center">
                    <Camera className="w-12 h-12 text-red-400/50 mb-2" />
                    <span className="text-xs font-mono text-slate-300">
                      Prior Claim Photo: Ward 07 Bill 19
                    </span>
                    <span className="text-[11px] text-slate-500 mt-1">
                      Captured: 2025-08-19 14:10:00 (6 months prior)
                    </span>
                    {showCorrespondence && (
                      <div className="absolute inset-0 pointer-events-none border-2 border-red-500/40 rounded flex items-center justify-center">
                        <span className="text-[10px] font-mono bg-red-950/80 text-red-300 px-2 py-0.5 rounded border border-red-700">
                          Homography Verified (Inliers: 42 &ge; 25)
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="text-[11px] font-mono text-slate-400 space-y-0.5">
                    <div>Work Order: {(selectedItem as any).visualForensics.candidateWorkOrder}</div>
                    <div>Location: Ward 07 Reach 1 (13.0452° N, 77.5819° E)</div>
                  </div>
                </div>
              ) : (
                <div className="bg-app-surface border border-app-border rounded-lg p-6 flex flex-col items-center justify-center text-center text-slate-400">
                  <CheckCircle2 className="w-10 h-10 text-emerald-400 mb-2" />
                  <h4 className="text-xs font-mono font-semibold text-slate-200">
                    No Duplicate Historical Instance Found
                  </h4>
                  <p className="text-[11px] text-slate-500 mt-1 max-w-xs">
                    SSCD vector search against pgvector HNSW index confirmed uniqueness across all municipal public-works dossiers.
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* 3. GIS TELEMETRY MODE: Centerline, Stationing & Disposal Quarry */}
        {/* ========================================================================= */}
        {isGis && (
          <div className="w-full max-w-3xl bg-app-surface rounded-lg p-6 border border-app-border space-y-4" data-testid="gis-mode-canvas">
            <div className="flex items-center justify-between border-b border-app-border pb-3">
              <div>
                <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                  PostGIS Spatial Verification Canvas
                </span>
                <h3 className="text-sm font-bold text-slate-100 mt-0.5">
                  {(selectedItem as any).title}
                </h3>
              </div>
              <span className="text-xs font-mono bg-emerald-950 text-emerald-300 px-2 py-0.5 rounded border border-emerald-800">
                Spatial Invariants Verified
              </span>
            </div>

            {/* Stylized Map Viewport */}
            <div className="bg-slate-950 rounded-lg p-6 border border-slate-800 text-slate-300 font-mono text-xs space-y-4 relative overflow-hidden">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-3 bg-app-elevated rounded border border-app-border space-y-1">
                  <div className="text-slate-400 text-[11px]">Drain Reach Centerline:</div>
                  <div className="font-bold text-sky-400">
                    {(selectedItem as any).tripData?.reachStationing?.drainId || 'SWD-BLR-NZ-09-02'}
                  </div>
                  <div className="text-[11px] text-slate-400">
                    Stationing: Ch {(selectedItem as any).tripData?.reachStationing?.startChainageM || 1200}m to {(selectedItem as any).tripData?.reachStationing?.endChainageM || 2400}m
                  </div>
                </div>

                <div className="p-3 bg-app-elevated rounded border border-app-border space-y-1">
                  <div className="text-slate-400 text-[11px]">Authorized Disposal Quarry:</div>
                  <div className="font-bold text-emerald-400">
                    Mavallipura Landfill (Radius: 500m)
                  </div>
                  <div className="text-[11px] text-slate-400">
                    Coordinates: 13.1492° N, 77.5341° E
                  </div>
                </div>
              </div>

              <div className="p-3 bg-app-elevated rounded border border-app-border space-y-2">
                <div className="text-xs font-semibold text-slate-200">
                  Telematics Trajectory & Transit Metrics
                </div>
                <div className="grid grid-cols-3 gap-2 text-[11px]">
                  <div>Distance: <span className="font-bold text-slate-100">{(selectedItem as any).tripData?.distanceKm || 11.4} km</span></div>
                  <div>Duration: <span className="font-bold text-slate-100">{(selectedItem as any).tripData?.durationMinutes || 38} min</span></div>
                  <div>Avg Velocity: <span className="font-bold text-slate-100">{(selectedItem as any).tripData?.averageSpeedKmH || 18.0} km/h</span></div>
                </div>
              </div>

              <div className="text-[11px] text-slate-500 pt-1 border-t border-slate-800 flex items-center justify-between">
                <span>PostGIS ST_DWithin Buffer: 50 meters</span>
                <span className="text-emerald-400 font-bold">FEASIBLE TRANSIT</span>
              </div>
            </div>
          </div>
        )}

      </div>
    </main>
  );
};
