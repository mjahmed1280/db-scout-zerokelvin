Docker PostgreSQL & Multi-Dataset Setup Guide

This document outlines the end-to-end process of setting up a PostgreSQL server in Docker on Windows, resolving port conflicts, and loading complex relational datasets (Olist & BikeStore) into a multi-schema architecture.

1. Environment Overview

Container Name: hackfest-postgres-final

Host Port: 5433 (Maps to internal container port 5432)

Database Name: hackfest_db

User: hackfest / hackfest123

Schemas: olist, bikestore, public

2. Docker Container Setup & Port Resolution

Initially, a local Windows PostgreSQL service occupied port 5432, preventing Docker from starting. We bypassed this by mapping the container to host port 5433.

Step 1: Create a Persistent Container with Shared Volumes

If data was already in a previous container (e.g., hackfest-postgres), we linked the volumes to ensure data persistence:

docker run --name hackfest-postgres-final ^
  -p 5433:5432 ^
  -e POSTGRES_PASSWORD=hackfest123 ^
  --volumes-from hackfest-postgres ^
  -d postgres


Step 2: Fix Authentication in the Database

To ensure external tools like VS Code could connect, we force-aligned the password internally:

docker exec -it hackfest-postgres-final psql -U hackfest -d hackfest_db
-- Run inside psql:
ALTER USER hackfest WITH PASSWORD 'hackfest123';
\q


3. Data Ingestion Architecture

Step 1: Preparing Docker Directories

Before copying files, directories must be created inside the container:

docker exec -it hackfest-postgres-final mkdir -p /data/olist
docker exec -it hackfest-postgres-final mkdir -p /data/bikestore


Step 2: Transferring CSVs from Windows

Using the docker cp command to move local datasets into the container:

:: Copy Olist Data
docker cp "C:\Path\To\olist-data\." hackfest-postgres-final:/data/olist

:: Copy BikeStore Data
docker cp "C:\Path\To\bikestore-data\." hackfest-postgres-final:/data/bikestore


4. Database Schema Design (SQL)

To avoid table name collisions (e.g., both datasets having a customers table), we implemented a Schema-per-Project architecture.

Creating the "Drawers"

CREATE SCHEMA IF NOT EXISTS olist;
CREATE SCHEMA IF NOT EXISTS bikestore;


Dataset 1: Olist (E-commerce)

Tables were created in the olist schema.

Example Table: olist.orders, olist.customers, olist.order_items.

Note: Moved from public using ALTER TABLE tablename SET SCHEMA olist;.

Dataset 2: BikeStore

Tables were created in the bikestore schema with strict Foreign Key constraints.

5. Final Loading Commands (The "COPY" Protocol)

PostgreSQL's COPY command was used for high-speed ingestion. We handled the common "NULL" string error found in Kaggle datasets.

Import Script

-- Example for Olist
COPY olist.customers FROM '/data/olist/olist_customers_dataset.csv' 
WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- Example for BikeStore (Handling literal 'NULL' strings in CSV)
COPY bikestore.products FROM '/data/bikestore/products.csv' 
WITH (FORMAT CSV, HEADER, NULL 'NULL');


Order of Import for BikeStore:

categories, brands, customers, stores (Parents)

products, staffs (Secondary)

orders, stocks (Tertiary)

order_items (Final)

6. Maintenance & Troubleshooting Commands

Command

Action

docker ps

Check if container is running on port 5433.

\dn

(psql) List all schemas.

\dt *.*

(psql) List all tables across all schemas.

SET search_path TO olist, bikestore;

Set default schemas for easier querying.

7. VS Code Connection (SQLTools)

Host: 127.0.0.1

Port: 5433

SSL: Disabled