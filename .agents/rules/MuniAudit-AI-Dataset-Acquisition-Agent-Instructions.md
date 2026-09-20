# MuniAudit-AI Dataset Acquisition Agent Instructions

**Project:** MuniAudit-AI  
**Purpose:** Automatically acquire, validate, organize, and prepare the dataset stack required by the locked MuniAudit-AI architecture.  
**Mode:** Automatic-first; manual fallback when automatic acquisition is unavailable.  
**Source basis:** `Multimodal Dataset Acquisition, Benchmarking, and Synthetic Linkage Strategy for MuniAudit-AI`  
**Status:** DATA ACQUISITION INSTRUCTION SPECIFICATION v1.0

---

## 1. Agent Mission

You are the dataset-acquisition and preparation agent for MuniAudit-AI.

Your primary task is to:

1. discover the required dataset assets from the approved research;
2. attempt automatic download/acquisition;
3. verify that the downloaded content matches the expected asset;
4. record provenance, URL, source, license information from the research;
5. organize files into the correct project directories;
6. never silently substitute an unrelated dataset;
7. report anything that could not be downloaded automatically;
8. generate precise manual-download instructions for any failed item;
9. prepare the acquired data for the MuniAudit-AI benchmark pipeline.

The agent must work from the approved dataset specification below.

---

# 2. Non-Negotiable Rules

## Rule 1 — Do not invent datasets

Only acquire datasets explicitly listed in this instruction or additional sources explicitly approved by the project owner.

## Rule 2 — Do not silently replace a failed source

If a URL fails, do not automatically substitute another dataset that "looks similar."

Instead:

- retry;
- investigate the official source page if network access is available;
- report the failure;
- provide a manual fallback.

## Rule 3 — Do not pretend synthetic data is real

The research explicitly defines several relationships as synthetic or simulated.

Maintain provenance labels:

- `REAL_MUNICIPAL_DATA`
- `REAL_INFRASTRUCTURE_DATA`
- `REAL_DOCUMENT_BENCHMARK`
- `REAL_TRANSPORT_DATA`
- `DERIVED_STATUTORY_DATA`
- `SYNTHETIC_DATA`
- `SIMULATED_DATA`
- `SYNTHETIC_LINK`
- `SIMULATED_LINK`

These labels must remain attached to the files and generated records.

## Rule 4 — Do not modify original source files

Keep original downloaded assets immutable.

Create processed copies in separate directories.

## Rule 5 — Do not download restricted government data by bypassing access controls

Do not:

- bypass CAPTCHAs;
- defeat authentication;
- scrape restricted portals;
- impersonate users;
- circumvent rate limits;
- use unofficial credentialed access.

The approved research explicitly says not to depend on live Vahan/Parivahan scraping.

## Rule 6 — Preserve attribution

For every source, store:

- source name;
- source URL;
- owner;
- license/terms as stated in the research;
- retrieval date;
- local filename;
- provenance category.

## Rule 7 — Fail safely

A failed download must never cause the pipeline to silently manufacture a replacement.

---

# 3. Expected Project Directory

Create:

```text
data/
├── raw/
│   ├── municipal/
│   │   └── bbmp_stormwater/
│   ├── visual/
│   │   └── rdd2022_india/
│   ├── documents/
│   │   └── sroie/
│   ├── transport/
│   │   └── delhi_otd/
│   └── statutory/
│       └── morth/
│
├── reference/
│   ├── vehicles/
│   ├── disposal_sites/
│   └── configuration/
│
├── processed/
│   ├── municipal/
│   ├── visual/
│   ├── documents/
│   ├── transport/
│   └── statutory/
│
├── synthetic/
│   ├── weighbridge/
│   ├── trips/
│   ├── dossiers/
│   └── anomalies/
│
├── annotations/
│   ├── visual/
│   ├── documents/
│   └── dossiers/
│
├── benchmark/
│   ├── calibration/
│   ├── test/
│   ├── hard_negatives/
│   └── manifests/
│
└── manifests/
    ├── dataset_manifest.json
    ├── acquisition_log.json
    ├── provenance.csv
    └── checksums.sha256
```

---

# 4. Approved Dataset Stack

## P0 — Primary spatial anchor

### BBMP Stormwater Drains KML

**Dataset role:** Real municipal drainage geometry.

**Research-specified source:**

```text
https://data.opencity.in/dataset/fc97e05c-c54b-44e9-8d98-7663ee887922/resource/114758e9-c356-46e0-afdb-e1d52f972863/download/03eea514-d4bf-4cd9-8c7b-f904b1ea83f2.kml
```

**Master complete-network source from research:**

```text
https://data.opencity.in/dataset/fc97e05c-c54b-44e9-8d98-7663ee887922/resource/801779e6-ed81-457d-bd2a-7e3cc95ad1ee/download/e42be0cb-1bf4-4a7b-9c78-0c0dbdae3237.kml
```

**Portal page:**

```text
https://data.opencity.in/dataset/bengaluru-stormwater-drains-maps
```

### Automatic acquisition

Preferred:

```bash
mkdir -p data/raw/municipal/bbmp_stormwater
curl -L --fail --retry 5 \
  -o data/raw/municipal/bbmp_stormwater/bbmp_stormwater_master.kml \
  "https://data.opencity.in/dataset/fc97e05e-.../e42be0cb-....kml"
```

Do not literally replace the URL with the abbreviated example above. Use the exact research URL recorded in the manifest.

Alternative:

```bash
wget -O data/raw/municipal/bbmp_stormwater/bbmp_stormwater_master.kml \
  "FULL_MASTER_KML_URL"
```

### Verify

Check:

- file exists;
- file is valid XML/KML;
- expected `<Placemark>` elements exist;
- coordinates parse correctly;
- geometry can be loaded with GeoPandas/Fiona;
- CRS is detected or explicitly assigned according to the source;
- no obvious truncation/corruption.

### Process

Create:

```text
data/processed/municipal/bbmp_stormwater/bbmp_stormwater.geojson
```

and, if needed:

```text
data/processed/municipal/bbmp_stormwater/bbmp_stormwater_postgis.sql
```

Preserve original KML.

---

# 5. P0 — Primary Visual Corpus

## RDD2022 India Subset

**Research-specified source:**

```text
https://github.com/sekilab/RoadDamageDetector
```

The research identifies the India subset as the primary real infrastructure visual corpus.

### Automatic acquisition strategy

First inspect the GitHub repository:

```bash
git clone --depth 1 \
  https://github.com/sekilab/RoadDamageDetector.git \
  data/raw/visual/rdd2022_india/RoadDamageDetector
```

Then inspect the repository README/release/data instructions for the actual India archive.

If a direct archive URL is provided by the repository, download it with resumable retrieval:

```bash
curl -L --fail --retry 5 -C - \
  -o data/raw/visual/rdd2022_india/RDD2022_India.zip \
  "DIRECT_ARCHIVE_URL"
```

### Important

Do NOT invent a direct URL if the repository does not expose one.

If automatic retrieval cannot resolve the official data archive:

1. report the repository URL;
2. report the exact manual step;
3. ask the user to download the India subset;
4. continue with other datasets.

### Verify

After download:

```bash
unzip -t data/raw/visual/rdd2022_india/RDD2022_India.zip
```

Confirm:

- archive is not corrupted;
- JPEG images are readable;
- corresponding annotation files exist where expected;
- image count can be measured;
- no unexpected executable files are present.

### Process

Create:

```text
data/processed/visual/rdd2022_india/images/
data/processed/visual/rdd2022_india/annotations/
```

Do NOT resize all source images destructively.

Create a separate benchmark preprocessing stage for:

```text
512 x 512
```

where required by the model pipeline.

---

# 6. P1 — Document Benchmark

## ICDAR 2019 SROIE

**Research-specified sources:**

```text
https://huggingface.co/datasets/jsdnrs/ICDAR2019-SROIE
```

and:

```text
https://huggingface.co/datasets/rth/sroie-2019-v2
```

### Automatic acquisition

Preferred Python/Hugging Face approach:

```bash
python -m pip install -U datasets huggingface_hub
```

Then use a small acquisition script or CLI.

Example:

```python
from datasets import load_dataset

ds = load_dataset(
    "jsdnrs/ICDAR2019-SROIE"
)

print(ds)
```

Save/export the required split to:

```text
data/raw/documents/sroie/
```

### Authentication

If Hugging Face requires a token for the chosen repository:

- do not put the token in source code;
- use environment variables or the local Hugging Face credential helper;
- never commit tokens.

### Verify

Check:

- images open;
- annotation/ground-truth records exist;
- fields are parseable;
- sample count;
- image/text pairing;
- duplicate files.

### Important

This is a **generic receipt benchmark**, not an Indian municipal weighbridge dataset.

Do not relabel it as municipal data.

It serves as a document-OCR baseline only.

---

# 7. P0 — MoRTH Statutory Data

## MoRTH S.O. 3467(E)

**Research-specified source:**

```text
https://morth.nic.in/
```

**Research also references:**

```text
https://www.i-cema.in/notification-s-o-3467e-16-07-2018-new-axle-weight-notification/
```

### Automatic acquisition

Prefer the official MoRTH source.

Search only the official website for:

```text
S.O. 3467(E)
16 July 2018
axle weight notification
```

Download the official Gazette/PDF if directly available.

### If automatic retrieval fails

Manual fallback:

1. Open the MoRTH website.
2. Search for the exact notification.
3. Download the Gazette PDF.
4. Save as:

```text
data/raw/statutory/morth/morth_so_3467e.pdf
```

### Process

Extract the relevant statutory tables into:

```text
data/processed/statutory/morth/morth_vehicle_weight_limits.csv
```

Recommended columns:

```text
vehicle_class
axle_configuration
max_axle_weight_t
gross_vehicle_weight_kg
source_reference
```

Do not invent values that are not present in the source.

---

# 8. P1 — Delhi Open Transit Data

## Delhi OTD

**Research-specified portal:**

```text
https://otd.delhi.gov.in/
```

**Research-specified API example:**

```text
https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb
```

**Research-specified mirror:**

```text
https://www.kaggle.com/datasets/adarshdubey001/delhi-bus-transit-data-enhanced-for-ml
```

### Automatic acquisition priority

1. Prefer an openly downloadable static dataset/mirror.
2. If the official portal exposes a directly downloadable dataset without requiring credentials, use that.
3. Do not attempt to bypass API authentication/rate limits.
4. Do not make live OTD availability a runtime dependency of the hackathon demo.

### Kaggle

Use Kaggle CLI only when credentials are already configured:

```bash
kaggle datasets download \
  -d adarshdubey001/delhi-bus-transit-data-enhanced-for-ml \
  -p data/raw/transport/delhi_otd
```

Then unzip:

```bash
unzip -o \
  data/raw/transport/delhi_otd/*.zip \
  -d data/raw/transport/delhi_otd/
```

If Kaggle credentials are unavailable:

- do not ask the agent to bypass authentication;
- report manual download as required.

### Critical provenance rule

Delhi OTD represents **bus/transit movement**, not municipal tipper-truck telematics.

Use it only as an empirical transportation baseline for simulation/benchmark construction.

Label downstream traces as:

```text
SIMULATED_LINK
```

not real municipal haulage records.

---

# 9. P2 — CAG Audit Evidence

## CAG Performance Audit Report No. 2 of 2021

**Research-specified URL:**

```text
https://cag.gov.in/en/audit-report/details/113317
```

### Automatic acquisition

Open the official CAG page and locate the downloadable report PDF.

Save:

```text
data/raw/statutory/cag/bbmp_swd_performance_audit_report_2_2021.pdf
```

### Process

Extract:

- audit observations relevant to storm-water drains;
- transport/haulage issues;
- measurement/bookkeeping issues;
- evidence-verification issues;
- any documented expenditure/quantity discrepancies.

Store manually verified excerpts in:

```text
data/processed/statutory/cag/audit_observations.json
```

### Important

This document is **institutional audit evidence**, not a machine-learning training dataset.

It is used to ground:

- problem context;
- anomaly typologies;
- audit wording;
- benchmark design.

---

# 10. Vehicle Registry Data

## Important: No live Vahan scraping

The dataset research explicitly states that live Vahan/Parivahan access should NOT be a runtime dependency.

Do not scrape or bypass Vahan access controls.

The research proposes a local reference database with approximately 2,500 realistic records.

### Automatic options

The agent may:

1. use an already-provided/approved open vehicle dataset;
2. use public statutory/manufacturer reference data where licensing permits;
3. create a clearly synthetic reference table.

### Required classification

Every record must be tagged:

```text
REAL
DERIVED
SYNTHETIC
```

### Synthetic vehicle schema

```text
vehicle_reg_no
vehicle_class
manufacturer
model
axle_configuration
ulw_kg
gvw_kg
body_type
body_volume_m3
registration_status
provenance
```

Do not fabricate that a synthetic vehicle registration is an actual government registration.

---

# 11. Weighbridge Receipts

## No large public municipal dataset was identified in the research

Therefore the agent must NOT waste time searching endlessly for a nonexistent public corpus.

Use:

```text
SROIE
+
procedural Indian weighbridge generator
+
thermal degradation engine
```

### Synthetic generator outputs

Create:

```text
data/synthetic/weighbridge/
├── images/
├── ground_truth/
├── manifests/
└── generation_config.yaml
```

Target:

```text
250 synthetic weighbridge vouchers
```

across multiple layout variants.

### Required fields

```text
ticket_number
weighbridge_id
vehicle_reg_no
gross_weight_kg
tare_weight_kg
net_weight_kg
timestamp
```

### Required anomaly types

```text
ARITHMETIC_MISMATCH
DUPLICATE_TICKET
VEHICLE_MISMATCH
THERMAL_DEGRADATION
MISSING_FIELD
```

### Critical provenance

Every generated receipt must be marked:

```text
SYNTHETIC_DATA
```

---

# 12. GPS / Trip Data

## No real municipal haulage corpus is established by the research

Therefore:

- do not pretend Delhi transit data is municipal truck data;
- use Delhi OTD only to estimate reasonable urban travel characteristics;
- generate synthetic truck trips connecting real spatial anchors.

### Output

```text
data/synthetic/trips/
├── gps/
├── manifests/
├── trip_records.csv
└── generation_config.yaml
```

Suggested fields:

```text
trip_id
vehicle_reg_no
dispatch_timestamp
site_arrival_timestamp
dump_arrival_timestamp
source_reach_id
assigned_dump_id
gps_trace_id
provenance
```

Generated trajectories must be marked:

```text
SIMULATED_DATA
SIMULATED_LINK
```

---

# 13. Disposal-Site Geometry

The approved research requires disposal-site polygons.

### Automatic-first

Search the approved project sources for publicly available municipal disposal-site geometry.

Accept only if:

- source is verified;
- coordinates are clear;
- licensing/access is clear.

### Manual/synthetic fallback

If no appropriate public geometry can be obtained:

- create a controlled benchmark configuration using clearly marked synthetic disposal polygons;
- store:

```text
provenance = SYNTHETIC_DATA
```

Do not claim the polygon represents a real landfill unless verified.

---

# 14. Benchmark Construction

After acquisition, the agent must create the benchmark inputs.

## Target

```text
MuniAudit-250
```

The research proposes a 250-dossier benchmark.

Recommended composition from the research:

```text
80  clean baseline controls
20  legitimate operational exceptions
30  visual copy/manipulation
25  scale arithmetic discrepancy
25  vehicle classification mismatch
25  kinematic violation
15  physical capacity overload
15  duplicate ticket
15  spatial corridor breach
```

Before finalizing counts, validate that the total is exactly 250.

### Each dossier should contain

```text
dossier_manifest.json
contract metadata
drain reach
photos
weighbridge evidence
vehicle reference
trip record
GPS trace
disposal site
ground-truth anomaly labels
provenance fields
```

---

# 15. Data Linkage Rules

Every relationship must be tagged.

## REAL LINK

Example:

```text
actual BBMP drain geometry
```

## DERIVED LINK

Example:

```text
vehicle class → statutory payload constraint
```

## SYNTHETIC LINK

Example:

```text
RDD2022 image → synthetic contract dossier
```

## SIMULATED LINK

Example:

```text
simulated truck GPS trajectory → real drain/disposal coordinates
```

Never collapse these categories.

---

# 16. Data Leakage Prevention

The agent preparing benchmark splits must preserve:

## Spatial holdout

Separate geographic training/calibration and test regions.

## Temporal holdout

Separate earlier and later synthetic/derived evidence where timestamps exist.

## Contractor holdout

Synthetic contractor/fleet identities must not appear across train and test if they can create memorization.

## Device holdout

Where image metadata/capture identities are simulated, prevent the same device signature from leaking across partitions.

## Receipt-template holdout

Keep at least one receipt layout/template isolated for testing.

## Near-duplicate holdout

Do not put original and transformed versions of the same image into different evaluation partitions.

---

# 17. Checksum and Provenance Manifest

Generate:

```text
data/manifests/dataset_manifest.json
```

Example structure:

```json
{
  "dataset": "BBMP Stormwater Drains KML",
  "source_url": "...",
  "downloaded_at": "...",
  "local_path": "...",
  "provenance": "REAL_MUNICIPAL_DATA",
  "license": "...",
  "sha256": "...",
  "size_bytes": 0,
  "verified": true
}
```

Generate a global:

```text
data/manifests/checksums.sha256
```

using:

```bash
sha256sum <file> >> data/manifests/checksums.sha256
```

---

# 18. Automatic Acquisition Script

Create:

```text
scripts/acquire_datasets.py
```

The script should:

1. create directories;
2. download publicly accessible P0/P1/P2 sources;
3. retry failed HTTP requests;
4. use resumable downloads for large files where possible;
5. verify MIME/type;
6. verify archive integrity;
7. calculate checksums;
8. write acquisition logs;
9. mark failures;
10. produce a manual fallback report.

Suggested CLI:

```bash
python scripts/acquire_datasets.py
```

Optional:

```bash
python scripts/acquire_datasets.py --only bbmp
python scripts/acquire_datasets.py --only rdd
python scripts/acquire_datasets.py --only sroie
python scripts/acquire_datasets.py --only otd
python scripts/acquire_datasets.py --only morth
python scripts/acquire_datasets.py --only cag
```

Never require the whole acquisition process to fail because one source is unavailable.

---

# 19. Manual Fallback Report

If any automatic acquisition fails, create:

```text
data/manifests/MANUAL_DOWNLOAD_REQUIRED.md
```

For every failed asset include:

```text
Dataset:
Priority:
Reason automatic acquisition failed:
Exact official/source URL:
Expected filename:
Expected approximate size:
Manual steps:
Destination directory:
Validation command:
```

Example:

```markdown
## RDD2022 India

Status: MANUAL DOWNLOAD REQUIRED

Source:
https://github.com/sekilab/RoadDamageDetector

Why:
Official India archive could not be resolved automatically.

Manual action:
Open the repository and follow the official dataset download instructions.

Expected destination:
data/raw/visual/rdd2022_india/

Validation:
unzip -t RDD2022_India.zip
```

---

# 20. Post-Download Validation Script

Create:

```text
scripts/validate_datasets.py
```

It must validate:

### BBMP

```text
KML parseable
Placemark count > 0
coordinates valid
geometry valid
```

### RDD2022

```text
images readable
annotations present
archive intact
```

### SROIE

```text
images readable
ground-truth available
pairing valid
```

### MoRTH

```text
PDF exists
text extractable or manually verified
```

### Delhi OTD

```text
CSV/GTFS parseable
required timestamp/location fields present
```

### CAG

```text
PDF accessible
relevant sections extractable
```

---

# 21. Do Not Treat Estimated Counts as Verified Counts

The research document contains approximate dataset volumes.

The acquisition agent must calculate the actual locally downloaded counts.

For example:

```text
Expected in research: ~9,665 images
Actual acquired: 9,xxx images
```

Record:

```text
expected_count
actual_count
count_verified = true/false
```

Do not silently report the research estimate as the actual local count.

---

# 22. Source-to-Project Mapping

After acquisition, generate:

```text
data/manifests/source_to_component.csv
```

with:

```text
source
modality
project_component
provenance
real_or_synthetic
license
local_path
status
```

Example:

```text
BBMP KML
GIS
PostGIS chainage
REAL_MUNICIPAL_DATA
...
```

---

# 23. What Must Be Automatically Downloaded

Attempt automatic acquisition for:

### P0

- BBMP Stormwater Drain KML
- RDD2022 India
- MoRTH S.O. 3467(E)

### P1

- SROIE
- Delhi OTD static data

### P2

- CAG report

Do this in priority order.

---

# 24. What Must Be Generated Locally

The acquisition agent must prepare or hand off generation for:

- synthetic weighbridge receipts;
- degraded thermal versions;
- synthetic trip manifests;
- synthetic GPS traces;
- synthetic contract IDs;
- synthetic contractor identities;
- synthetic anomaly injections;
- benchmark dossiers;
- benchmark metadata.

These are not "downloads."

They are controlled dataset-generation tasks.

---

# 25. What Must NOT Be Automatically Scraped

Never scrape:

```text
Vahan / Parivahan restricted data
private municipal databases
private contractor systems
authenticated portals without approved credentials
CAPTCHA-protected sources
```

---

# 26. Recommended Acquisition Order

Execute:

```text
1. BBMP KML
2. RDD2022
3. SROIE
4. MoRTH Gazette
5. CAG report
6. Delhi OTD
7. validate all sources
8. generate vehicle reference data
9. generate weighbridge data
10. generate trip/GPS data
11. assemble linked dossiers
12. inject controlled anomalies
13. create holdout splits
14. generate provenance manifests
```

---

# 27. Stop Conditions

The agent may declare the dataset acquisition phase COMPLETE only when:

- all automatically accessible P0 datasets are acquired and validated;
- failed automatic sources have manual instructions;
- all required synthetic generators are identified;
- provenance is recorded;
- checksums exist;
- original files are preserved;
- the benchmark can be assembled without claiming synthetic data is real;
- no restricted dataset has been bypassed.

---

# 28. Final Acquisition Readiness Report

Create:

```text
data/manifests/DATASET_READINESS_REPORT.md
```

with:

```text
# Dataset Readiness

## Acquired Automatically
...

## Acquired Manually
...

## Synthetic Required
...

## Missing / Blocked
...

## Validation Results
...

## License / Provenance Notes
...

## Benchmark Readiness
...

## Remaining Manual Actions
...
```

End the report with exactly one status:

```text
DATA_READY
```

or:

```text
DATA_READY_WITH_MANUAL_ITEMS
```

or:

```text
DATA_BLOCKED
```

---

# 29. Final Expected State

At the end, the repository should contain something approximately like:

```text
data/
├── raw/
│   ├── municipal/bbmp_stormwater/
│   ├── visual/rdd2022_india/
│   ├── documents/sroie/
│   ├── transport/delhi_otd/
│   └── statutory/{morth,cag}/
│
├── processed/
│   ├── municipal/
│   ├── visual/
│   ├── documents/
│   ├── transport/
│   └── statutory/
│
├── synthetic/
│   ├── weighbridge/
│   ├── trips/
│   ├── dossiers/
│   └── anomalies/
│
├── benchmark/
│   ├── calibration/
│   ├── test/
│   └── hard_negatives/
│
├── annotations/
└── manifests/
    ├── dataset_manifest.json
    ├── acquisition_log.json
    ├── provenance.csv
    ├── checksums.sha256
    ├── MANUAL_DOWNLOAD_REQUIRED.md
    └── DATASET_READINESS_REPORT.md
```

---

# 30. Final Instruction to the Agent

Execute automatically wherever technically and legally possible.

When automatic acquisition fails, DO NOT improvise.

Instead:

1. preserve the failure details;
2. provide the exact manual download URL/steps;
3. continue acquiring every other available dataset;
4. validate everything that was successfully obtained;
5. clearly identify the remaining manual task.

The agent's success criterion is not:

> "It downloaded something."

The success criterion is:

> **"The exact approved MuniAudit-AI dataset stack is reproducibly acquired, validated, provenance-tagged, organized, and ready for benchmark construction without misrepresenting synthetic or generic datasets as real municipal evidence."**