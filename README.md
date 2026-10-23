# AI-Powered Finance Decision Support Assistant – Team 1

A conversational assistant for financial analysts, built on **IBM watsonx Orchestrate** with a **Supabase (PostgreSQL)** data layer. Analysts ask finance questions in plain English and get a calculated answer, the working, and a source for every figure. All data is synthetic.

> **Project status:** Sprint 3 complete and handed over. Two agent versions are provided, **3.0.1** (latest, with downloadable PDF analysis) and **2.0.5** (stable, without the PDF tool). See [Agent versions](#agent-versions).

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Example Questions](#example-questions)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Agent Versions](#agent-versions)
- [Getting Started](#getting-started)
- [Data](#data)
- [Synthetic Data Generation](#synthetic-data-generation)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Project Timeline](#project-timeline)
- [Scope](#scope)
- [Known Issues](#known-issues)
- [Team](#team)

---

## Overview

Financial analysts spend a large share of their time collecting and consolidating data before they can analyse it. This assistant lets them ask questions in natural language and returns:

- the result of the calculation,
- the formula and the steps used,
- the source of every figure (file, row and column),
- relevant policy and market context, with citations, and
- a short plain-language summary.

When data is missing, invalid or would cause a division by zero, the assistant **refuses to calculate**, says which value is the problem, and asks the analyst to verify it. It never guesses.

**Target users:** Financial Analysts (direct users) and CFOs (consume the outputs).

## Key Features

- **Six financial calculations:** Dollar Variance, Percentage Variance, Gross Margin, Period-over-Period Growth, Year-over-Year Growth and Variance Contribution by Category.
- **Traceability:** every figure in a table carries a Source column (`source_file`, `source_row`, `source_column`).
- **Safe handling of bad data:** missing values, zero denominators, negative values and non-numeric values are surfaced, not hidden.
- **Policy and market context:** material variances are explained with cited, probabilistic market context. The assistant says so when nothing relevant exists.
- **Scope guard:** questions outside the six calculations or outside 2025–2026 get a clear "unavailable" message with examples of what to ask.
- **Downloadable analysis (3.0.1 only):** the analysis can be downloaded as a PDF.
- **Synthetic data only:** no real or confidential data is used.

## Example Questions

- "What is the dollar variance for revenue in March 2026?"
- "How did our gross margin change from Q1 2026 to Q2 2026?"
- "What is the year-over-year growth in Marketing expenses for 2026?"
- "Which expense category contributed most to the operating expense variance in Q2 2026?"

The data contains deliberately seeded edge cases. For example, the gross margin question above should be refused because February 2026 revenue is zero.

## How It Works

```
Analyst  →  watsonx Orchestrate agent  →  5 OpenAPI tools  →  Supabase PostgreSQL
              (instructions, guidelines,
               knowledge base)
```

1. The analyst asks a question in the Orchestrate chat.
2. The agent checks it is in scope, then calls the data tools for the exact monthly rows it needs.
3. It applies the formula, refuses if the inputs are missing or invalid, and builds the answer with a Source column.
4. If the variance is material, it adds market context and business-rule thresholds.
5. In 3.0.1, the analyst can ask for the analysis as a downloadable PDF.

The five tools are `get2025Records`, `get2026Records`, `getCategories`, `getMarketContext` and `getBusinessRules`. Quarterly and yearly figures are always derived from exactly three or twelve monthly rows.

## Tech Stack

| Layer | Technology |
|---|---|
| Agent and chat interface | IBM watsonx Orchestrate (agent builder, knowledge base, OpenAPI tools) |
| Data store | Supabase (PostgreSQL), accessed through the OpenAPI tools |
| Synthetic data | Python 3 (`data/scripts/generate_synthetic_data.py`) |
| PDF download (3.0.1) | IBM PDF generator tool in Orchestrate |
| Design | Figma (personas, wireframes, conversation workflows) |
| Superseded (Sprint 1) | IBM Planning Analytics, with MDX backed up in `docs/pa-backup` |

## Agent Versions

The agent is backed up in [`src/finance_assistant/backups/`](src/finance_assistant/backups/). Both versions use the same tables, the same OpenAPI tool file, the same knowledge base and the same guidelines. They differ only in the **agent Instructions** and the **IBM PDF generator tool**.

| Version | Folder | PDF download | Status |
|---|---|---|---|
| **3.0.1** (latest) | [`backups/3.0.1`](src/finance_assistant/backups/3.0.1) | Yes | All validation, edge-case and privacy testing was done on this version. Has the two PDF-tool issues in [Known Issues](#known-issues). |
| **2.0.5** (stable) | [`backups/2.0.5`](src/finance_assistant/backups/2.0.5) | No | Earlier stable build without the PDF tool. Not covered by the same testing. |

Each version folder contains the agent `Description`, `Instructions`, `Guidelines`, `KnowledgeBase`, `Tables`, `Tools` and `Connections` exports.

## Getting Started

The assistant runs inside watsonx Orchestrate, so there is nothing to host. To reproduce it, you rebuild the agent in your own account from the backup files. The project was built on free trial accounts, so a trial is enough, but trials expire.

### Prerequisites

- Git
- Python 3 (only to run the synthetic data generator)
- An IBM watsonx Orchestrate account where you can create agents
- A Supabase account (a free project is enough)

### 1. Clone the repository

```bash
git clone https://github.com/donovan-ong/IBM-Finance-Decision-Support-Assistant-Team-1.git
cd IBM-Finance-Decision-Support-Assistant-Team-1
```

### 2. Try the synthetic data generator (optional)

```bash
python3 data/scripts/generate_synthetic_data.py
```

This is only to see how the data was produced. You do not need to run it, because the finished tables are already in [`data/processed/`](data/processed/) and in each backup folder.

### 3. Create the database

Create a Supabase project, create the five tables (`financial_data_2025`, `financial_data_2026`, `categories`, `market_context`, `business_rules`) and import the CSVs from `src/finance_assistant/backups/<version>/Tables`.

### 4. Recreate the agent

Pick a version folder, then in Orchestrate create an agent named *Finance Decision Support Assistant* and fill it from that folder:

1. Paste `Description.txt` and `Instructions.txt`.
2. Paste the four guidelines from `Guidelines/`.
3. Upload the files in `KnowledgeBase/` to the knowledge base, keeping the same grouping.
4. Import `Tools/supabase_openapi3.json` as an OpenAPI tool. **Edit its server URL to point at your own Supabase project first**, then set API-key authentication with your own key.
5. Follow `Connections/Supabase Financial DB Connection.txt` and the screenshots to set up the connection.
6. For 3.0.1 only, enable the IBM PDF generator tool.
7. Test in Draft Preview, then deploy.

### Secrets

There is no `.env` file. The only secrets are your Supabase URL and API key, entered in Orchestrate. **Never commit them.**

### Checking it works

- Each Supabase table returns rows, and the `financial_data_*` tables have `source_file`, `source_row` and `source_column` filled in.
- Ask: "How did our gross margin change from Q1 2026 to Q2 2026?" The agent should refuse because February 2026 revenue is zero.
- Ask a variance question for a valid month. The answer should include a Source column and state that the data is synthetic.
- Ask about a period outside 2025–2026. The agent should say it is unavailable.
- (3.0.1 only) Ask for the analysis as a download and open the PDF.

## Data

The assistant reads five Supabase tables. The finished CSVs for each are tracked in [`data/processed/`](data/processed/).

| Table | Contents |
|---|---|
| `financial_data_2025`, `financial_data_2026` | Monthly Actual and Budget values per category, with `source_file`, `source_row` and `source_column` for traceability |
| `categories` | Revenue, Cost of Goods Sold and five expense categories, with their group |
| `market_context` | Public economic indicators (ABS, RBA, World Bank, ESC Victoria) for 2025-01 to 2026-09, with source and notes |
| `business_rules` | One row per rule: category thresholds and verification guidance |

Missing values are stored as `NULL` and are never defaulted to 0.

## Synthetic Data Generation

Only synthetic data is permitted, so the project includes a script that generates a realistic, reproducible dataset.

**Script:** [`data/scripts/generate_synthetic_data.py`](data/scripts/generate_synthetic_data.py)

```bash
python3 data/scripts/generate_synthetic_data.py
```

- **Raw output** is written to `data/raw/`, which is gitignored. Regenerate it locally instead of pulling it from git.
- **Finished datasets** (hand-adjusted and used by the agent) are tracked in `data/processed/`. A fresh run will not match them exactly.

**How the numbers are made:** Revenue and each expense category follow a compounding monthly growth trend (their Budget value), and the Actual value is that trend plus random noise with category-specific volatility (Rent is stable, Marketing is volatile). Cost of Goods Sold is a fixed percentage of Revenue's budget. Everything is controlled by named constants at the top of the script (`RANDOM_SEED`, `REVENUE_PROFILE`, `EXPENSE_PROFILES`, `COGS_TO_REVENUE_RATIO`).

**Seeded edge cases:** 18 cells are overwritten on purpose, covering missing values, division by zero, negative values and non-numeric values, so the calculation rules have known-bad inputs to be tested against.

**Reproducibility:** the output is deterministic for a fixed `RANDOM_SEED` (default `42`). See [`docs/calculations/Synthetic_Data_Formula_Verification.md`](docs/calculations/Synthetic_Data_Formula_Verification.md) for the reference command, worked examples of all six calculations and a table of where each edge case is seeded.

## Repository Structure

```
.
├── data/
│   ├── processed/            Final tables used by the agent (CSV, tracked)
│   └── scripts/              Synthetic data generator
├── design/
│   ├── conversation_workflows/   Conversation flows for the assistant
│   └── wireframes/planning_analytics/   Sprint 1 dashboard wireframes
├── docs/
│   ├── ai_logs/              Record of AI assistance used on the project
│   ├── business-rules/       Business rules and thresholds
│   ├── calculations/         Formulas and synthetic data verification
│   ├── five-question/        Question set used to test the assistant
│   ├── market-context/       Market context data and policy
│   ├── pa-backup/            Planning Analytics backup (MDX and rules), Sprint 1
│   ├── policy/               Synthetic data and governance policies
│   └── requirements/         Requirements, user stories and data specification
├── src/finance_assistant/
│   ├── backups/              Agent exports: 3.0.1 (latest) and 2.0.5 (stable)
│   ├── calculations/         Early Python prototype of the variance calculations
│   └── orchestrate/tools/    OpenAPI specification for the Supabase tools
├── tests/unit/               Unit tests for the Python prototype
├── .gitignore
└── README.md
```

The Python code in `src/finance_assistant/calculations` and `tests/unit` was an early prototype. The live assistant does not use it. Calculations are performed by the agent from its instructions and the formulas in `docs/calculations`.

## Requirements

Full requirements, user stories and acceptance criteria are in [`docs/requirements`](docs/requirements).

## Project Timeline

| Sprint | Focus | What was delivered |
|---|---|---|
| **1 – Design & Bootstrap** | Environment and design | Synthetic data and policy, Planning Analytics cube and MDX calculations, personas, wireframes and conversation workflows |
| **2 – Raw MVP** | Core functionality | Orchestrate agent with the CSV knowledge base, first end-to-end answers |
| **3 – Refine MVP** | Hardening | Moved data to Supabase with OpenAPI tools for exact, traceable retrieval, guidelines for edge cases and privacy, testing, risk register, and the downloadable PDF analysis |

The knowledge-base approach in Sprint 2 reported valid months as missing, which is why Sprint 3 moved to Supabase.

## Scope

**In scope:** six core calculations, source traceability for every figure, policy and market context, short analysis summaries, and synthetic data under a defined policy.

**Out of scope:** real or confidential data, autonomous or multi-agent systems, integration with IBM internal tools beyond the brief, a mobile app, browsers other than Chrome and Safari, financial transactions, and finance questions outside the defined use cases.

**Assumptions and constraints:** English only; tested in Chrome and Safari; only synthetic or publicly licensed data; web-based; built on the IBM product stack; delivered within 9 weeks.

## Known Issues

- **Intermittent data access (3.0.1 only):** since the PDF tool was added, the agent sometimes says it cannot view the record for a period that exists. Refreshing the agent a few times usually fixes it. The cause is not known.
- **PDF formatting (3.0.1 only):** some PDFs show square boxes where a hyphen (`-`) should be. This is intermittent and the cause is not known.
- **Run-to-run variation:** the model does the retrieval and calculation, so answers can vary between runs.
- **Accounts are temporary:** the agent was built on free trial accounts and a team Supabase project. Rebuild it in your own accounts using [Getting Started](#getting-started).

If the PDF issues matter, use version **2.0.5**, which has no PDF tool.

## Team

| Role | Assigned To |
|---|---|
| Project Manager | Jack Robinson-Fletcher |
| Business Analyst | Raghdah Al-Gahdari |
| UX Designer | Monika Swiergon |
| Developer | Donovan Ong |
| Developer | Mike Jayilian |

**Client / Organization:** Aaron / IBM
