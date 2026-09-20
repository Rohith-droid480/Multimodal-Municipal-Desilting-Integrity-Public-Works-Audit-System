import React from 'react';
import { EvidenceItem } from '@/types/evidence';
import { EpistemicBadge } from '@/components/ui/epistemic-badge';
import { Camera, FileText, Truck, MapPin, CheckCircle, AlertTriangle, HelpCircle } from 'lucide-react';

interface EvidenceTreeProps {
  evidenceList: EvidenceItem[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

export const EvidenceTree: React.FC<EvidenceTreeProps> = ({
  evidenceList,
  selectedId,
  onSelect,
}) => {
  const photos = evidenceList.filter((e) => e.type === 'SITE_PHOTO' || e.type === 'HISTORICAL_PHOTO');
  const receipts = evidenceList.filter((e) => e.type === 'WEIGHBRIDGE_RECEIPT');
  const trips = evidenceList.filter((e) => e.type === 'VEHICLE_TRIP');

  const renderItem = (item: EvidenceItem) => {
    const isSelected = item.id === selectedId;
    let Icon = FileText;
    if (item.type.includes('PHOTO')) Icon = Camera;
    if (item.type === 'VEHICLE_TRIP') Icon = Truck;

    return (
      <button
        key={item.id}
        onClick={() => onSelect(item.id)}
        className={`w-full text-left p-2 rounded-md transition-all text-xs border ${
          isSelected
            ? 'bg-app-active/80 border-app-border-focus text-slate-100 shadow-xs'
            : 'bg-app-elevated/40 border-app-border text-slate-300 hover:bg-app-elevated hover:text-slate-100'
        }`}
        data-testid={`evidence-tree-item-${item.id}`}
      >
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1.5 min-w-0">
            <Icon className="w-3.5 h-3.5 shrink-0 text-sky-400" />
            <span className="font-mono text-[11px] truncate font-medium">{item.id}</span>
          </div>
          <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-400 border border-slate-700 shrink-0">
            {item.provenance}
          </span>
        </div>
        <p className="text-xs text-slate-300 mt-1 line-clamp-1">{item.title}</p>
        <div className="mt-1 flex items-center justify-between text-[11px] text-slate-500 font-mono">
          <span>{new Date(item.submittedAt).toLocaleDateString('en-IN')}</span>
          <EpistemicBadge category={item.epistemicInfo.category} />
        </div>
      </button>
    );
  };

  return (
    <aside className="w-80 bg-app-surface border-r border-app-border flex flex-col shrink-0 overflow-y-auto">
      <div className="p-3 border-b border-app-border bg-app-surface/90 sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-mono font-semibold uppercase tracking-wider text-slate-300">
            Evidence Tree ({evidenceList.length})
          </h2>
          <span className="text-[10px] font-mono text-slate-500">
            PROVENANCE TRACKED
          </span>
        </div>
      </div>

      <div className="p-3 space-y-4">
        {/* Site Photographs */}
        <div>
          <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 mb-2">
            <Camera className="w-3.5 h-3.5 text-sky-400" />
            <span>Site Photographs ({photos.length})</span>
          </div>
          <div className="space-y-1.5">{photos.map(renderItem)}</div>
        </div>

        {/* Weighbridge Slips */}
        <div>
          <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 mb-2">
            <FileText className="w-3.5 h-3.5 text-amber-400" />
            <span>Weighbridge Receipts ({receipts.length})</span>
          </div>
          <div className="space-y-1.5">{receipts.map(renderItem)}</div>
        </div>

        {/* Vehicle Trips & GPS */}
        <div>
          <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 mb-2">
            <Truck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Vehicle & GPS Logs ({trips.length})</span>
          </div>
          <div className="space-y-1.5">{trips.map(renderItem)}</div>
        </div>
      </div>
    </aside>
  );
};
