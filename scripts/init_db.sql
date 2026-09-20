-- MuniAudit-AI PostgreSQL Extension Initialization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;
-- PostGIS extension can be enabled if the postgis image is combined with pgvector
CREATE EXTENSION IF NOT EXISTS postgis;
