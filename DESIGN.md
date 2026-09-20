# MuniAudit-AI — Forensic UI Design Specification (DESIGN.md)

**System Identity:** MuniAudit-AI Forensic Audit Console  
**Aesthetic Profile:** High-density, dark slate forensic evidence inspection workspace  
**Design Principle:** Evidence clarity and audit provenance override decorative effects.

---

## 1. Color Tokens & Theme Architecture

The UI strictly operates on a curated Slate/Zinc dark palette designed to reduce eye strain during prolonged evidentiary inspection:

### Background & Surface Hierarchy
- **Canvas Base:** `#090D16` (Deep Obsidian / Midnight Slate)
- **Panel Surface (Level 1):** `#0F172A` (Slate 900)
- **Card / Viewport Surface (Level 2):** `#1E293B` (Slate 800)
- **Elevated Hover / Border:** `#334155` (Slate 700)
- **Subtle Dividers:** `#1E293B`

### Epistemic Status Badges
- **FACT:** Neutral Slate Badge (`bg-slate-800 text-slate-200 border-slate-600`)
- **MODEL_OUTPUT:** Violet/Purple Badge (`bg-purple-950/60 text-purple-300 border-purple-800`)
- **RULE_RESULT:** Cyan/Sky Badge (`bg-sky-950/60 text-sky-300 border-sky-800`)
- **INFERENCE:** Amber Badge (`bg-amber-950/60 text-amber-300 border-amber-800`)
- **RECOMMENDATION:** Emerald/Teal Badge (`bg-emerald-950/60 text-emerald-300 border-emerald-800`)

### Administrative Determination Tokens
- **VERIFIED_COMPLIANT:** Emerald (`#10B981` / `bg-emerald-950 text-emerald-400`)
- **SUBSTANTIVE_INCONSISTENCY:** Crimson/Rose (`#F43F5E` / `bg-rose-950 text-rose-400`)
- **INCONCLUSIVE_DATA:** Amber/Orange (`#F59E0B` / `bg-amber-950 text-amber-400`)
- **TECHNICAL_ABSTENTION:** Gray/Muted (`#64748B` / `bg-slate-900 text-slate-400`)

---

## 2. Typography & Density

- **Font Family:** Inter, Roboto, or SF Pro Display (`sans-serif`)
- **Monospace Font:** JetBrains Mono or Fira Code (for SHA-256 digests, GPS coordinates, timestamps, and JSON payloads)
- **Layout Density:** Compact/Forensic (8px base grid, compact table paddings, zero wasted whitespace)

---

## 3. Core Workspace Layout (3-Column Architecture)

```text
┌────────────────────────┬──────────────────────────────────┬────────────────────────┐
│ 1. Dossier Navigator   │ 2. Dual-Viewport Evidence Canvas │ 3. Finding & Triage    │
│                        │                                  │                        │
│ - Evidence Tree        │ - Left: Submitted Photo / Ticket │ - Epistemic Category   │
│ - Provenance Tags      │ - Right: Historical / Spatial    │ - Observed vs Expected │
│ - SHA-256 Hashes       │ - SIFT Feature Link Overlays     │ - Auditor Review Radio │
│ - Upload Metadata      │ - Leaflet GIS Reach Polygon      │ - Sign-off Action Bar  │
└────────────────────────┴──────────────────────────────────┴────────────────────────┘
```
