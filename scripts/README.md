# Data Quality & Automated Ingestion Pipeline

## 📌 Project Overview
This project demonstrates an automated Python ingestion script that acts as an enterprise-grade **Data Quality Gate**. It intercepts incoming API streams, applies operational validation rules, filters out null or corrupted rows, and loads only validated payloads into a data warehouse.

## 🏗️ Technical Stack
* **Language:** Python 3 (Validation Engine)
* **Target Warehouse:** PostgreSQL
* **Infrastructure:** Docker Compose

## 💡 SSIS Translation: The Data Quality Advantage
In legacy architectures, filtering rows requires dragging and dropping **SSIS Conditional Splits** or setting up **Error Output Redirects** to separate tables. This project translates that behavior entirely into clean, unit-testable Python code. Building programmatic quality gates allows teams to dynamically adjust validation rules via code without redeploying massive compilation packages.
