### **Workload Profile and Operational Capacity Model**

To evaluate the cost, latency, and performance of MuniAudit-AI on AWS, the operational envelope is modeled across low, midpoint, and peak bounds for a 1–10 user municipal audit deployment.

The transaction lifecycle assumes audit dossiers containing high-resolution visual evidence (mobile camera photographs) alongside scanned thermal weighbridge vouchers.

&nbsp;

&nbsp;

&nbsp;

\+-------------------------------------------------------------------------------------------------+  
| WORKLOAD SCALE ENVELOPE (HACKATHON & EARLY PILOT TIERS)                                         |  
\+----------------------------------------------------+--------------+--------------+--------------+  
| Metric Parameter                                   | Low Bound    | Midpoint     | Peak Bound   |  
\+----------------------------------------------------+--------------+--------------+--------------+  
| Active Administrative Users                        | 1            | 5            | 10           |  
| Processed Audit Dossiers / Day                     | 10           | 50           | 100          |  
| Visual Evidence Photographs / Dossier              | 10           | 30           | 50           |  
| Thermal Weighbridge Documents / Dossier            | 5            | 10           | 20           |  
| Daily Image Ingestion Volume                       | 100 images   | 1,500 images | 5,000 images |  
| Daily Document Ingestion Volume                    | 50 docs      | 500 docs     | 2,000 docs   |  
| Monthly Dossier Volume (30-day billing cycle)      | 300 dossiers | 1,500 dos.   | 3,000 dos.   |  
| Monthly Visual Images (avg. 2 MB / image)          | 9,000 (18 GB)| 45,000 (90GB)| 150,000(300G)|  
| Monthly Document Scans (avg. 1 MB / scan)          | 1,500 (1.5GB)| 15,000 (15GB)| 60,000 (60GB)|  
| 72-Hour Active Hackathon Sprint Volume             | 30 dossiers  | 150 dossiers | 300 dossiers |  
| 72-Hour Sprint Storage Footprint                   | \~1.95 GB     | \~9.75 GB     | \~19.50 GB    |  
\+----------------------------------------------------+--------------+--------------+--------------+

### **Comparative Evaluation of Architectural Paradigms**

Selecting an AWS deployment model requires balancing the fixed baseline cost floor, cold-start latency overhead, horizontal scalability, and developer maintenance burden for a 1–4 person engineering team.

&nbsp;

&nbsp;

&nbsp;

\+-------------------------------------------------------------------------------------------------+  
| ARCHITECTURAL PARADIGM TRADE-OFF MATRIX                                                         |  
\+----------------------------------------------------+--------------+--------------+--------------+  
| Evaluation Vector                                  | Serverless   | Container    | Managed ML   |  
|                                                    | (Lambda/Step)| (App Runner) | (SageMaker)  |  
\+----------------------------------------------------+--------------+--------------+--------------+  
| Baseline Monthly Cost Floor (Idle State)           | \~$25 \- $30   | \~$35 \- $60   | \~$1,100+     |  
| Cold-Start Latency (p95)                           | 1.2s \- 2.8s  | \< 50 ms      | 5s \- 15s     |  
| Burst Scaling Velocity                             | Instantaneous| Moderate     | Auto-scaling |  
| Local Development & Testing Parity                 | Moderate     | High         | Low          |  
| Operational Maintenance Overhead                   | Low          | Low          | High         |  
| Hackathon Suitability (Time to Ship)               | High         | Very High    | Poor         |  
\+----------------------------------------------------+--------------+--------------+--------------+

#### **Pure Serverless (AWS Lambda \+ Step Functions \+ Textract \+ RDS PostgreSQL)**

* Mechanism: Event-driven execution where incoming Amazon S3 evidence uploads trigger Step Functions Express Workflows, invoking specialized Lambda containers (packaged with OpenCV and ONNX Runtime) to extract embeddings and perform spatial calculations.

* Advantages: Costs scale directly to zero when idle; fully managed high availability; no server patching or capacity planning.  
* Trade-offs: Container cold starts (1.2 to 2.8 seconds) on initial image processing; 15-minute maximum function execution ceiling; ephemeral memory constraints.

#### **Container-Centric (AWS App Runner / ECS Fargate \+ RDS PostgreSQL)**

* Mechanism: A unified containerized web and worker application (e.g., FastAPI or Streamlit backend) running on AWS App Runner or Amazon ECS Fargate, connecting directly to Amazon S3 and an Amazon RDS PostgreSQL instance.

* Advantages: High local development parity (identical Docker container runs locally and in the cloud); zero cold starts once provisioned; direct in-memory caching of feature embeddings; straightforward long-running model execution.

* Trade-offs: Persistent memory provisioning fee on App Runner ($0.007 per GB-hour idle) creates a non-zero monthly baseline cost.

#### **Managed ML & Enterprise Search (SageMaker Endpoints \+ OpenSearch Serverless \+ Aurora)**

* Mechanism: Dedicated SageMaker Real-Time inference endpoints for visual copy detection, Amazon OpenSearch Serverless for vector similarity search, and Amazon Aurora Serverless v2 for relational data.  
* Advantages: High throughput for enterprise workloads; automated model endpoint monitoring; decoupled vector storage.  
* Trade-offs: Prohibitive minimum cost floor. SageMaker Real-Time GPU endpoints (ml.g5.xlarge) cost approximately $737 per month idle, while OpenSearch Serverless enforces a minimum baseline of 2 OpenSearch Compute Units (OCUs) costing approximately $345 per month. This model represents an expensive anti-pattern for hackathons and early-stage pilots.

### **Detailed Subsystem Cost and Performance Estimation**

The pricing model below contrasts published AWS list rates (US East, N. Virginia, us-east-1) against projected expenditures across the three operational workload tiers over a standard 30-day billing cycle, as well as a focused 72-hour hackathon demonstration sprint.

&nbsp;

&nbsp;

&nbsp;

\+-------------------------------------------------------------------------------------------------+  
| PUBLISHED AWS COMPONENT PRICING REFERENCE (US-EAST-1)                                           |  
\+--------------------------------+----------------------------------------------------------------+  
| AWS Service Component          | Published List Price (On-Demand)                               |  
\+--------------------------------+----------------------------------------------------------------+  
| Amazon S3 Standard Storage     | $0.023 per GB-month                                            |  
| Amazon S3 API Requests         | PUT/POST: $0.005 per 1,000; GET: $0.0004 per 1,000             |  
| Amazon API Gateway (HTTP API)  | $1.00 per 1,000,000 requests                                   |  
| AWS Lambda Compute (ARM)       | $0.0000133334 per GB-second; $0.20 per 1,000,000 invocations   |  
| AWS Step Functions (Express)   | $1.00 per 1,000,000 executions; $0.00001667 per GB-second      |  
| Amazon Textract (Queries API)  | $0.015 to $0.025 per page ($15.00 to $25.00 per 1,000 pages)   |  
| Amazon Bedrock (Nova Micro)    | $0.035 per 1M input tokens; $0.14 per 1M output tokens         |  
| Amazon Bedrock (Claude Haiku)  | $1.00 per 1M input tokens; $5.00 per 1M output tokens          |  
| Amazon RDS db.t4g.small        | $0.032 to $0.034 per hour (\~$23.04 to $24.48/month) \[cite: 6, 7\]           |  
| Amazon RDS db.t4g.micro        | $0.016 per hour (\~$11.52/month)                                |  
| Amazon RDS GP3 Storage         | $0.115 per GB-month                                            |  
| AWS App Runner vCPU / Memory   | Active: $0.064/vCPU-hr; Idle Memory: $0.007/GB-hr \[cite: 2, 4, 5\]               |  
| Amazon CloudWatch Ingestion    | $0.50 per GB ingested (First 5 GB/month free)                  |  
\+--------------------------------+----------------------------------------------------------------+

&nbsp;

&nbsp;

&nbsp;

\+--------------------------------------------------------------------------------------------------+  
| ESTIMATED 30-DAY MONTHLY SUBSYSTEM COST AT WORKLOAD TIERS                                        |  
\+-----------------------------+-------------------+--------------------+---------------------------+  
| Subsystem Component         | Low Bound (10/day)| Midpoint (50/day)  | Peak Bound (100/day)      |  
\+-----------------------------+-------------------+--------------------+---------------------------+  
| Evidence Storage (S3)       | $0.46             | $2.55              | $8.50                     |  
| Document Intelligence (OCR) | $22.50 (Textract) | $225.00 (Textract) | $900.00 (Textract)        |  
| Document OCR (Self-Hosted)  | $0.00 (Lambda CPU)| $0.00 (Lambda CPU) | $1.20 (Lambda CPU)        |  
| ML Inference (SSCD on ONNX) | $0.00 (Free Tier) | $0.00 (Free Tier)  | $2.40 (Lambda ARM)        |  
| Vector Search & Database    | $25.34 (RDS small)| $25.34 (RDS small) | $27.64 (RDS \+ 40GB GP3)   |  
| API Ingress & Routing       | $0.02             | $0.10              | $0.35                     |  
| Orchestration & Business CS | $0.05             | $0.25              | $0.85                     |  
| Generative AI (Bedrock)     | $0.05 (Haiku)     | $0.25 (Haiku)      | $1.10 (Haiku)             |  
| Observability & Logs        | $0.00 (Free Tier) | $0.50              | $2.00                     |  
\+-----------------------------+-------------------+--------------------+---------------------------+  
| Total Estimated Cost        |                   |                    |                           |  
| (with Amazon Textract)      | \~$48.42 / month   | \~$254.00 / month   | \~$943.00 / month          |  
| Total Estimated Cost        |                   |                    |                           |  
| (with Local PaddleOCR)      | \~$25.92 / month   | \~$29.00 / month    | \~$44.20 / month           |  
\+-----------------------------+-------------------+--------------------+---------------------------+

#### **Storage & Evidence Ingestion (Amazon S3)**

* Published Pricing: $0.023 per GB-month for Standard S3; $0.005 per 1,000 PUT requests; $0.0004 per 1,000 GET requests.  
* Workload Application: At the midpoint workload (50 dossiers/day), 45,000 images (90 GB) and 15,000 receipts (15 GB) generate 105 GB of cumulative evidence per month.  
* Cost Calculation: $105 \\times \\$0.023 \= \\$2.41$ for storage. 60,000 PUT requests cost $\\$0.30$. 200,000 verification GET queries cost $\\$0.08$.  
* Estimated Total: $2.79 per month. For a 72-hour hackathon demo sprint (\~10 GB), storage costs are under $0.25.

#### **Document Intelligence & OCR Extraction**

* Published Pricing: Amazon Textract AnalyzeDocument with Queries API costs $0.015 per page (up to 1M pages/month).  
* Workload Application: At 50 dossiers/day and 10 documents/dossier, volume is 500 pages/day or 15,000 pages/month.  
* Managed Cost: $15{,}000 \\times \\$0.015 \= \\$225.00$ per month.  
* Low-Cost Self-Hosted Alternative: Packaging PaddleOCR PP-OCRv4 inside an AWS Lambda container (2048 MB memory, execution latency \~120 ms on CPU). Compute costs for 15,000 invocations: $15{,}000 \\times 0.12\\text{ s} \\times 2\\text{ GB} \= 3{,}600\\text{ GB-seconds}$, which falls entirely within the AWS Lambda Free Tier (400,000 GB-seconds per month).  
* Estimated Total: $22.50 for a 72-hour hackathon run on Textract (1,500 documents), or $0.00 using local containerized PaddleOCR.

#### **Visual Copy-Detection Inference (SSCD Feature Extraction)**

* Published Pricing: AWS Lambda Graviton2 (ARM) compute at $0.0000133334 per GB-second.  
* Workload Application: The Meta SSCD ResNet-50 model compiled to ONNX format (95 MB) executes inside an AWS Lambda container allocated 3072 MB memory (provisioning \~1.8 vCPUs). Inference latency measures \~80 ms per image.  
* Cost Calculation: At 45,000 images/month: $45{,}000 \\times 0.08\\text{ s} \\times 3\\text{ GB} \= 10{,}800\\text{ GB-seconds}$. The AWS Lambda Free Tier covers up to 400,000 GB-seconds and 1,000,000 requests monthly.  
* Estimated Total: $0.00 net cost under the free tier; approximately $0.15 per month if the free tier is exhausted.

#### **Vector Search and Relational Spatial Storage (Amazon RDS PostgreSQL)**

* Published Pricing: Amazon RDS db.t4g.small (2 vCPU, 2 GB RAM, Graviton2) costs $0.034 per hour in us-east-1. GP3 storage costs $0.115 per GB-month.

* Workload Application: A single RDS instance with both postgis and pgvector enabled supports spatial chainage projections (ST\_LineLocatePoint) and HNSW vector similarity search over 512-dimensional embeddings. 20 GB of GP3 storage easily accommodates 150,000 embedding records (512 dimensions in FP32 \= 2,048 bytes per record, requiring \~307 MB raw vector storage plus \~40 MB index overhead).  
* Cost Calculation: Compute: $730\\text{ hours} \\times \\$0.034 \= \\$24.82$. Storage: $20\\text{ GB} \\times \\$0.115 \= \\$2.30$.  
* Estimated Total: $27.12 per month. If using db.t4g.micro (1 GB RAM, suitable for local demo datasets under 10,000 vectors), compute drops to $0.016 per hour, bringing the monthly total to $13.98. For a 72-hour hackathon, running a db.t4g.small costs exactly $72 \\times \\$0.034 \= \\$2.45$.

#### **API Ingress and Request Orchestration**

* Published Pricing: Amazon API Gateway HTTP API costs $1.00 per million requests. AWS Step Functions Express Workflows cost $1.00 per million executions and $0.00001667 per GB-second.  
* Workload Application: At 50 dossiers/day, API calls total approximately 250,000 requests/month. Express workflow executions total 50,000 per month with an average execution duration of 450 ms at 128 MB allocation.  
* Estimated Total: HTTP API: $0.25. Step Functions Express: $0.05 \+ \\$0.04 \= \\$0.09$. Total: \~$0.34 per month.

#### **Generative AI Audit Synthesis (Amazon Bedrock)**

* Published Pricing: Anthropic Claude 3.5 Haiku on Bedrock costs $1.00 per 1M input tokens and $5.00 per 1M output tokens. Amazon Nova Micro costs $0.035 per 1M input tokens and $0.14 per 1M output tokens.  
* Workload Application: Synthesizing administrative summaries from structured JSON contradiction payloads requires \~800 input tokens and \~200 output tokens per finding. Generating summaries for 1,500 dossiers/month consumes 1.2M input tokens and 300K output tokens.  
* Cost Calculation:  
  * Using Claude 3.5 Haiku: $(1.2 \\times \\$1.00) \+ (0.3 \\times \\$5.00) \= \\$1.20 \+ \\$1.50 \= \\$2.70$ per month.  
  * Using Amazon Nova Micro: $(1.2 \\times \\$0.035) \+ (0.3 \\times \\$0.14) \= \\$0.042 \+ \\$0.042 \= \\$0.08$ per month.  
* Estimated Total: $0.08 to $2.70 per month.

#### **Observability & Logging (Amazon CloudWatch)**

* Published Pricing: Ingestion costs $0.50 per GB; first 5 GB per month is free.  
* Workload Application: Structured JSON application logs generate approximately 50 KB per dossier, totaling \~2.5 MB/day or \~75 MB/month, which falls comfortably within the free tier.  
* Estimated Total: $0.00.

### **Architectural Anti-Patterns: Expensive and Unnecessary Components**

To preserve a lean cost profile during hackathon development and pilot validation, several common enterprise cloud patterns must be avoided.

&nbsp;

&nbsp;

&nbsp;

\+-------------------------------------------------------------------------------------------------+  
| UNNECESSARY & EXPENSIVE AWS COMPONENTS TO AVOID                                                 |  
\+-----------------------------+--------------------+---------------------+------------------------+  
| Avoided Component           | Fixed Idle Cost    | Primary Defect      | Recommended Lean       |  
|                             | Floor / Month      | at Hackathon Scale  | Alternative Component  |  
\+-----------------------------+--------------------+---------------------+------------------------+  
| AWS NAT Gateway             | \~$32.40 / AZ       | Expensive routing tax; Lambda Function URLs;   |  
|                             | (+ $0.045/GB)      | drains budget idle  | public subnets on demo |  
| SageMaker Real-Time GPU     | \~$737.00 / month   | Underutilized GPU   | AWS Lambda ARM (ONNX)  |  
| (ml.g5.xlarge)              |                    | running 24/7 idle   | or local CPU inference |  
| Amazon OpenSearch           | \~$345.60 / month   | 2 OCU minimum       | PostgreSQL extension   |  
| Serverless                 | (2 OCUs base)     | capacity floor    | pgvector on RDS       |  
| Amazon Aurora Serverless v2 | \~$43.80 / month    | 0.5 ACU baseline    | Amazon RDS PostgreSQL  |  
|                             | (0.5 ACU min)      | cost floor          | db.t4g.small ($23/mo) \[cite: 7\]  |  
| Amazon Kendra / Enterprise  | \~$810.00 / month   | Closed enterprise   | Bedrock with structured|  
| Search Index                | (Developer tier)   | indexing unneeded   | JSON context prompts  |  
| AWS RDS Proxy               | \~$11.00 / month    | Connection pooling  | Client-side pool       |  
|                             | per vCPU allocated | overhead unneeded   | limits in Lambda       |  
\+-----------------------------+--------------------+---------------------+------------------------+

> 1. AWS NAT Gateway: Deploying AWS Lambda functions inside a custom VPC to communicate with private RDS instances requires provisioning a NAT Gateway so the functions can reach external AWS services (S3, Textract, Bedrock). A NAT Gateway incurs a fixed idle charge of $0.045 per hour ($32.40/month per Availability Zone) plus $0.045 per GB processed.  
   * Alternative: For hackathons, deploy Lambda functions outside the VPC and connect to RDS over SSL using an authorized IP security group or assign Lambda Function URLs directly. Alternatively, run the application container in a public subnet on AWS App Runner with egress-only VPC connectors.  
> 2. Amazon OpenSearch Serverless: Enforces an idle reservation of at least 1 Indexing OCU and 1 Search OCU ($0.24/OCU-hour), generating a baseline charge of \~$345 per month even with zero search traffic.  
   * Alternative: Enable the pgvector extension directly inside PostgreSQL.  
> 3. SageMaker Real-Time Inference: Allocating a dedicated GPU instance (ml.g5.xlarge) costs $1.01 per hour ($737/month) regardless of whether requests are actively being processed.  
   * Alternative: Export deep learning models to ONNX and run inference on CPU-based Lambda functions or within the primary application container.

### **The Recommended Low-Cost "Ship-It" Architecture**

The recommended architecture balances cost efficiency, deployment simplicity, and genuine AWS integration, pairing a containerized application runtime on AWS App Runner with managed database and serverless extraction services.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

User Web Browser (Streamlit UI / Leaflet Map)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼ (HTTPS / TLS 1.3 Termination)  
AWS App Runner (1 vCPU, 2 GB RAM Container) ◄──── Auto-Deploys via GitHub or ECR  
&nbsp;&nbsp;│  
&nbsp;&nbsp;├── Local FastAPI Core & Worker Services:  
&nbsp;&nbsp;│     ├── OpenCV Normalization (Bilateral Filter, CLAHE, Deskew)  
&nbsp;&nbsp;│     ├── SSCD Feature Extraction (ONNX Runtime CPU, 512d FP32)  
&nbsp;&nbsp;│     ├── Spatial Verification (OpenCV SIFT \+ RANSAC Homography)  
&nbsp;&nbsp;│     ├── Geospatial Routing Engine (Haversine & OSRM Distance Lookups)  
&nbsp;&nbsp;│     ├── Deterministic Invariant Engine (Gross \- Tare \= Net Validation)  
&nbsp;&nbsp;│     └── In-Memory L1 Cache (Active Contract Feature Vectors)  
&nbsp;&nbsp;│  
&nbsp;&nbsp;├──► Amazon S3 Standard (Raw Images, Scale Scans, PDF/A Dossiers)  
&nbsp;&nbsp;│  
&nbsp;&nbsp;├──► Amazon Textract API (AnalyzeDocument Queries for Thermal Vouchers)  
&nbsp;&nbsp;│      └── Fallback: Embedded PaddleOCR ONNX Worker  
&nbsp;&nbsp;│  
&nbsp;&nbsp;├──► Amazon Bedrock API (Amazon Nova Micro / Claude 3.5 Haiku for Memos)  
&nbsp;&nbsp;│  
&nbsp;&nbsp;└──► Amazon RDS PostgreSQL db.t4g.small (Single-AZ, 20 GB gp3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── PostGIS Extension (LineStringM Drain Centerlines & Geofences)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── pgvector Extension (512d HNSW Index on Contract Work Evidence)

#### **Operational Workflow Execution Trace**

> 1. Ingestion: The user uploads an audit dossier through the App Runner web UI. The application streams the binary directly to Amazon S3, calculating the SHA-256 digest on the fly.

> 2. Local Feature Extraction: For visual work evidence, the App Runner container invokes an embedded ONNX Runtime instance to extract the 512-dimensional SSCD vector in \~75 ms without external network calls.

> 3. Unified Vector and Spatial Match: The container executes a single SQL query against Amazon RDS PostgreSQL:

&nbsp;

&nbsp;

&nbsp;

SQL

SELECT image\_id, contract\_id,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1 \- (embedding \<=\> :query\_vector) AS cosine\_similarity,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ST\_LineLocatePoint(reach\_geom, ST\_SetSRID(ST\_MakePoint(:lon, :lat), 4326)) \* ST\_Length(reach\_geom) AS chainage\_m  
FROM municipal\_evidence  
WHERE contract\_id \= :active\_contract\_id  
ORDER BY embedding \<=\> :query\_vector ASC  
LIMIT 10;

> 4. Document Processing: Scale receipts are dispatched to the Amazon Textract Queries API to extract weights, vehicle IDs, and timestamps. If Textract experiences transient throttling, the container falls back to an embedded PaddleOCR ONNX worker.  
> 5. Invariant Gate: The container evaluates mathematical constraints ($\\text{Gross} \- \\text{Tare} \= \\text{Net}$) and spatial travel times deterministically in Python.  
> 6. Summary Generation: Verified contradiction payloads are formatted and passed to Amazon Bedrock (Nova Micro), which generates an objective audit memo in under 800 ms.  
> 7. Persistence: The finalized case status, calculation residuals, and W3C PROV-O metadata are committed to PostgreSQL.

### **Comprehensive Budget Breakdown: Monthly Baseline Versus 72-Hour Hackathon Sprint**

&nbsp;

&nbsp;

&nbsp;

\+--------------------------------------------------------------------------------------------------+  
| COMPREHENSIVE COST LEDGER: RECOMMENDED ARCHITECTURE (APP RUNNER \+ RDS \+ S3 \+ BEDROCK)           |  
\+-----------------------------+-----------------------+--------------------+-----------------------+  
| AWS Service Component       | Sizing & Configuration| Estimated Monthly  | Estimated 72-Hour     |  
|                             | Parameter Specification| Cost (Midpoint)    | Hackathon Demo Cost   |  
\+-----------------------------+-----------------------+--------------------+-----------------------+  
| AWS App Runner Compute      | 1 vCPU, 2 GB RAM      | $36.20             | $4.50                 |  
|                             | ($0.064/vCPU-hr act., | (Assumes 8 hrs/day | (Assumes 12 hrs/day   |  
|                             | $0.007/GB-hr idle) \[cite: 2, 4, 5\] | active, 16 hrs idle) | active demo testing)  |  
| Amazon RDS PostgreSQL       | db.t4g.small (Single- | $27.12             | $2.45                 |  
|                             | AZ, 20 GB gp3)       | (Runs 24/7 all mo.)| (3 days running)      |  
| Amazon S3 Storage & API     | Standard S3 (105 GB   | $2.79              | $0.25                 |  
|                             | cumulative, 60k PUTs) |                    | (\~10 GB demo files)   |  
| Amazon Textract API         | Queries API (15k pages| $225.00            | $15.00                |  
|                             | /mo; 1k demo pages)   |                    | (1,000 pages tested)  |  
| Amazon Bedrock Generative AI| Amazon Nova Micro     | $0.08              | $0.02                 |  
|                             | (1,500 dossier memos) |                    | (300 demo dossiers)   |  
| Amazon CloudWatch Logs      | Ingestion & Metrics   | $0.00 (Free Tier)  | $0.00                 |  
\+-----------------------------+-----------------------+--------------------+-----------------------+  
| Total Net Cloud Expenditure | Fully Managed System  |                    |                       |  
| (with Amazon Textract)      |                       | \~$291.19 / month   | \~$22.22 (Sprint Total)|  
| Total Net Cloud Expenditure |                       |                    |                       |  
| (with Local PaddleOCR)      | Zero-OCR API Ingestion| \~$66.19 / month    | \~$7.22 (Sprint Total) |  
\+-----------------------------+-----------------------+--------------------+-----------------------+

### **Latency Budget and Performance Optimization**

To deliver a responsive demonstration interface suitable for live auditor interactions, latency budgets are established across the verification lifecycle:

&nbsp;

&nbsp;

&nbsp;

\+-------------------------------------------------------------------------------------------------+  
| END-TO-END PIPELINE LATENCY BUDGET (TARGET p95: \< 3.5 SECONDS)                                  |  
\+-----------------------------+--------------------+-------------------+--------------------------+  
| Processing Subsystem Stage  | Execution Substrate| Latency Target    | Optimization Strategy    |  
\+-----------------------------+--------------------+-------------------+--------------------------+  
| Evidence Upload & Hashing   | S3 Pre-Signed URL  | 150 ms \- 250 ms   | Direct client-to-S3      |  
| Image Normalization (CLAHE) | App Runner (OpenCV)| 25 ms \- 45 ms     | In-memory numpy array    |  
| Visual Embedding (SSCD 512d)| ONNX Runtime (CPU) | 65 ms \- 85 ms     | Quantized INT8 / FP32    |  
| Vector Search & LRS Locate  | RDS PostgreSQL     | 8 ms \- 15 ms      | HNSW index \+ GiST R-Tree |  
| Document OCR (Textract)     | Amazon Textract    | 1,800 ms \- 2,500ms| Parallel async execution |  
| Spatial RANSAC Verification | App Runner (OpenCV)| 35 ms \- 60 ms     | Capped keypoint limits   |  
| Invariant Evaluation Engine | Pure Python        | \< 2 ms            | Pre-compiled validation  |  
| Generative Memo (Bedrock)   | Amazon Nova Micro | 450 ms \- 750 ms   | Streamed response token  |  
\+-----------------------------+--------------------+-------------------+--------------------------+

By packaging OpenCV, ONNX Runtime, and spatial algorithms directly within an AWS App Runner container and consolidating vector similarity and GIS calculations inside Amazon RDS PostgreSQL, the architecture delivers a scalable, performant auditing engine while keeping total infrastructure expenditure under $25 for the entire hackathon lifecycle.

&nbsp;