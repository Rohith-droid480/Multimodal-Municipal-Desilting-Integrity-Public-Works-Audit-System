import { EpistemicMetadata } from './epistemic';

export type EvidenceType =
  | 'SITE_PHOTO'
  | 'HISTORICAL_PHOTO'
  | 'WEIGHBRIDGE_RECEIPT'
  | 'INVOICE'
  | 'MEASUREMENT_BOOK'
  | 'VEHICLE_TRIP'
  | 'GPS_OBSERVATION'
  | 'DRAIN_GEOMETRY';

export type EvidenceProvenance =
  | 'REAL_MUNICIPAL'
  | 'REAL_PUBLIC'
  | 'DERIVED'
  | 'SYNTHETIC'
  | 'SIMULATED'
  | 'CONTROLLED_CAPTURE';

export interface BoundingBox {
  fieldKey: string;
  fieldLabel: string;
  value: string;
  confidence: number;
  isAmbiguous?: boolean;
  /** Normalized coordinates [ymin, xmin, ymax, xmax] in [0, 1] range */
  box: [number, number, number, number];
}

export interface BaseEvidenceItem {
  id: string;
  dossierId: string;
  type: EvidenceType;
  title: string;
  description: string;
  provenance: EvidenceProvenance;
  submittedAt: string;
  fileUrl?: string;
  mimeType: string;
  sha256Hash: string;
  metadata: Record<string, unknown>;
  epistemicInfo: EpistemicMetadata;
}

export interface SitePhotoEvidence extends BaseEvidenceItem {
  type: 'SITE_PHOTO' | 'HISTORICAL_PHOTO';
  cameraMetadata?: {
    make?: string;
    model?: string;
    dateTimeOriginal?: string;
    latitude?: number;
    longitude?: number;
    altitude?: number;
  };
  visualForensics?: {
    candidatePhotoUrl?: string;
    candidateDossierId?: string;
    candidateWorkOrder?: string;
    sscdSimilarity: number;
    ransacInliers: number;
    inlierThreshold: number;
    similarityThreshold: number;
    correspondenceVerified: boolean;
    candidateTimestamp?: string;
    candidateGps?: { lat: number; lng: number };
  };
}

export interface WeighbridgeEvidence extends BaseEvidenceItem {
  type: 'WEIGHBRIDGE_RECEIPT';
  extractedData?: {
    ticketNumber?: string;
    vehicleNumber?: string;
    grossWeightKg?: number;
    tareWeightKg?: number;
    netWeightKg?: number;
    calculatedNetKg?: number;
    arithmeticValid?: boolean;
    timestamp?: string;
    weighbridgeName?: string;
    ocrConfidence?: number;
  };
  pagination?: {
    totalPages: number;
    processedPages: number[];
    unprocessedPages: number[];
    preservationGapNote?: string;
  };
  boundingBoxes?: BoundingBox[];
}

export interface VehicleTripEvidence extends BaseEvidenceItem {
  type: 'VEHICLE_TRIP';
  tripData?: {
    vehicleNumber: string;
    startLocation: { lat: number; lng: number };
    endLocation: { lat: number; lng: number };
    distanceKm: number;
    durationMinutes: number;
    averageSpeedKmH: number;
    tripTimestamp: string;
    reachStationing: {
      drainId: string;
      startChainageM: number;
      endChainageM: number;
    };
    bufferValidation: {
      drainBufferMeters: number;
      disposalQuarryRadiusMeters: number;
      isWithinBuffer: boolean;
    };
  };
}

export type EvidenceItem = 
  | SitePhotoEvidence 
  | WeighbridgeEvidence 
  | VehicleTripEvidence 
  | BaseEvidenceItem;
