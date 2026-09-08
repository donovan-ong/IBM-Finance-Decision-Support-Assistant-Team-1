# Synthetic Data Policy

| | |
|---|---|
| **Document ID** | POL-DATA-001 |
| **Version** | 1.0 |
| **Status** | Proposed / Pending Approval |
| **Owner** | Raghdah AL-Gahdari, Business Analyst |
| **Approved by** | [pending] |
| **Last updated** | 2026-08-31 |
| **Applies to** |AI Finance Decision Support — Team 1, built for IBM |

---

## 1. Purpose

This policy defines the requirements and safeguards governing the use of **synthetic data** in the development, testing, and demonstration of the AI Finance Decision Support.

Its sole purpose is to ensure that:
> All data used by or referenced in this project is fully artificial, and at no point is real, confidential, commercially sensitive, or personally identifiable information used, stored, or exposed.

**This policy does not define financial or business logic** such as determining what constitutes a material variance or defining the business considerations relevant to a finding. These rules and considerations are defined separately in **business-rules.md and** **market-context.md**. The assistant uses these sources to provide analysis and decision support, while final business decisions remain with the appropriate human decision-makers. This separation is intentional and is further described in Section 6.

---

## 2. Scope

This policy applies to:
- All datasets used to train, test, evaluate, or demonstrate the Assistant.
- All data referenced in prompts, examples, or documentation shared as part of this project (including this GitHub repository).
- Any data the Assistant generates, transforms, or displays during a session.

It covers the financial fields currently defined in the project schema: **Revenue, COGS, Payroll Expense, Marketing Expense, Rent Expense, Utilities Expense, Other Expense**, each with `Actual_Value` and `Budget_Value`, on a monthly basis across 2025–2026.

---

## 3. Policy Statements

**P1 — No real data.**
No dataset used anywhere in this project may be derived from, copied from, or be traceable to an identifiable real company, individual, client, or transaction. All financial figures must be entirely synthetic in origin.

**P2 — No incidental exposure.**
Real company data, client data, or personal data must not be uploaded to this repository, entered into prompts, used in few-shot examples, or included in project documentation. This restriction applies even when the data is used temporarily, for testing, demonstration, comparison, or validation purposes.

**P3 — Data must remain financially plausible.**
While no real data is used, generated data must remain internally consistent and reflect plausible financial time-series characteristics, including **trends, controlled random variation, defined scenario variations or shocks where applicable, and logical relationships between line items**. Implausible or purely random data may reduce the reliability and usefulness of the Assistant's evaluation. The detailed data-generation methodology is maintained separately.


**P4 — Method must be explainable.**
The synthetic data generation technique must be sufficiently simple to be described, reproduced, and audited in plain language. Black-box generative methods (e.g., GANs and VAEs) are explicitly out of scope for this project. The project uses a rule-based statistical approach, as implemented and documented in the synthetic data generation script.

**P5 — Reproducibility.**
Data generation scripts must support the use of a fixed random seed and produce identical outputs when the same seed and generation parameters are used. This ensures that datasets can be consistently regenerated, reproduced, and independently verified.


**P6 — Transparency to the end user.**
When asked about the origin or nature of the data it is using, the Assistant must clearly state that the data is synthetic and must never imply the data represents a real organisation.

---

## 4. How the AI Assistant Must Use This Policy

When the Assistant is asked about the source, realism, or provenance of the data it is using, it must:

1. **Clearly identify the dataset as synthetic** and state that it was generated in accordance with this policy (`synthetic-data-policy.md`).

2. **Refer questions about the financial rationale or behaviour of a specific value** (e.g., “Why did Marketing Expense increase in July?”) to the relevant business-logic source. This policy defines data provenance and generation requirements; it does not define or explain the underlying financial or business behaviour.

3. **Never claim, imply, or create the impression that any data value represents a real company, client, individual, transaction, or other real-world entity.**


**Example — Correct Assistant Behaviour**

> “This dataset is fully synthetic and was generated in accordance with `synthetic-data-policy.md` (P1–P3). It does not represent any real company or individual. The reason July’s Marketing Expense was flagged is determined by the applicable rules in `business-rules.md`.”

**Example — Incorrect Assistant Behaviour**

> “Based on this data, it appears to represent a real mid-sized retailer that experienced a poor quarter.”

This distinction is important because it maintains a clear separation between **data-integrity and provenance claims**, which are governed by this policy, and **financial analysis and reasoning**, which are governed by the relevant business rules and market-context sources. This boundary ensures that the Assistant provides decision support based on defined project rules without presenting synthetic data as evidence of a real-world company or financial situation.


---

## 5. Relationship to Other Governing Documents

| Document | Governs | Owner |
|---|---|---|
| `synthetic-data-policy.md` (this file) | Data provenance, synthetic-data requirements, and confidentiality assurance | Business Analyst |
| `business-rules.md` | Materiality thresholds, variance logic, and the rules governing the Assistant's analysis and decision-support outputs, including behaviours that are deterministic or require AI judgemen | Business Analyst |
| `market-context.md` | Industry and seasonality assumptions used to inform scenario data generation and financial analysis | Business Analyst |
| `data/scripts/generate_synthetic_data.py`| The technical generation method used to produce the synthetic dataset, including the fixed-seed reproducibility (P5) and rule-based statistical approach (P4) required by this policy| Technical team, reviewed by BA |

This policy is the **authoritative source for the use, provenance, and confidentiality of the project’s data**. It establishes that the data used by the Assistant is synthetic and defines the requirements for its appropriate use and representation. It does not define the financial meaning of the data or the rules used to analyse it. Those responsibilities are covered by the relevant governing documents, including `business-rules.md`, `market-context.md`, and `data-generation-methodology.md`.

The Assistant must keep these responsibilities separate when analysing data or citing project sources. This policy must be used only to support claims about the **source and synthetic nature of the data**, while financial conclusions and analysis must be supported by the applicable financial and business rules. The Assistant is a **decision-support tool**: it provides analysis and relevant information to support human decision-making, but it does not make or approve business decisions on behalf of users.

---

## 6. Architectural Note (Context Only)

The Assistant combines **deterministic, custom-built functions with generative AI capabilities**. Deterministic functions may be used for defined and repeatable operations, such as applying established thresholds or calculation rules. Generative AI may be used to interpret results and provide explanations or contextual information within the scope defined by the project.

Regardless of how an output is generated, all outputs must comply with the requirements of P1–P6 of this policy. The method used to produce an output does not change the requirements relating to data provenance, synthetic-data use, confidentiality, or the accurate representation of the dataset.

The allocation of specific functions between deterministic logic and generative AI is governed by business-rules.md. This section provides architectural context only and does not define financial rules, analytical criteria, or the appropriate response to a particular finding.

The Assistant remains a **decision-support system**. Its outputs are intended to support human analysis and decision-making and must not be presented as autonomous business decisions or approvals.

---

## 7. Governance

- Any change to this policy requires a version increment and an entry in the changelog below.
- Changes must be reviewed against the project's confidentiality and privacy requirements before merging.
- This document supersedes any informal or verbal agreement about data sourcing for this project.

### Changelog

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-08-31 | Initial version; scope narrowed to data-provenance assurance per instructor guidance, separated from business/financial rules | Raghdah Al-Gahdari |

---

## 8. Related Project Documents

- Internal research: [`synthetic-data-research.docx`](https://rmiteduau.sharepoint.com/:w:/r/sites/CapstoneProgrammingProject2026-03-IBM-AIFinanceDecisionSupportTeam1/_layouts/15/Doc.aspx?action=edit&sourcedoc=%7Bc44c6575-f03c-4643-8e37-1662b807fa1f%7D&wdExp=TEAMS-TREATMENT&web=1) — *Team-internal SharePoint link; access restricted to project members with RMIT credentials.*
- Business rules: `business-rules.md`
- Market/industry context: `market-context.md`

## 9. External References
- Generating synthetic structured data | IBM watsonx. (n.d.-b). https://dataplatform.cloud.ibm.com/docs/content/wsj/synthetic/synthetic_data_overview_sd.html?context=wx

- Quick start: Generate synthetic tabular data | IBM watsonx. (n.d.-c). https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/get-started-generate-data.html?context=wx
