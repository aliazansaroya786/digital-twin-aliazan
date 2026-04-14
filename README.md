# Digital Twin — Ali Azan

> An AI-powered Digital Twin built on RAG (Retrieval-Augmented Generation) that conducts professional job interviews on behalf of Ali Azan using real career data stored in a vector database.

---

## About

| Field | Detail |
|---|---|
| **Student** | Ali Azan |
| **Course** | Bachelor of Business Information Systems Management (Minor in Accounting) |
| **University** | Victoria University, Sydney NSW |
| **Project** | AI Data Analyst Industry Project — Digital Twin |
| **Status** | ✅ Complete and tested |

---

## Project Overview

When an AI agent is given a job description, it retrieves real evidence from Ali Azan's career history stored in Upstash Vector Database and responds accurately on his behalf using STAR format answers, then generates a scored interview report with a pass/fail recommendation.

**Tested result:** 86% — STRONG PASS against Junior Business Analyst role at TechBridge Australia.

---

## How It Works

```
Job Description Input
        │
VS Code Agent Mode (GitHub Copilot)
        │
MCP Tool Call ──► rag_search()
        │
Upstash Vector Database (19 profile chunks, bge-large-en-v1.5)
        │
Retrieved Career Evidence (chunk IDs + similarity scores)
        │
STAR Format Answer (first person, evidence-cited)
        │
Pass/Fail Report (score out of 100%)
```

Every interview answer is grounded in retrieved vector chunks —
the agent cannot answer without first calling `rag_search()`.

---

## Technology Stack

| Component | Technology |
|---|---|
| Vector Database | Upstash Vector |
| Embedding Model | bge-large-en-v1.5 |
| LLM / Agent | GitHub Copilot Agent Mode (VS Code Insider) |
| MCP Framework | FastMCP (Python) |
| Project Manager | ClickUp |
| Version Control | GitHub |
| Language | Python 3.13 |

---

## Repository Structure

```
digital-twin-aliazan/
├── mcp_server.py              # MCP server exposing rag_search() tool
├── embed_profile.py           # Embeds profile.json into Upstash Vector
├── agents.md                  # Agent behaviour rules and interview instructions
├── README.md                  # This file
├── .env                       # Secret keys (never commit to GitHub)
├── .vscode/
│   └── mcp.json               # Registers MCP server with VS Code Insider
├── data/
│   └── profile.json           # Ali Azan's career data (19 chunks)
├── jobs/
│   └── sample-job.md          # Sample job description for testing
└── docs/
    ├── prd.md
    ├── design.md
    └── implementation-plan.md
```

---

## Setup Instructions

### Prerequisites
- VS Code Insider Edition
- GitHub Copilot Pro subscription
- Upstash Vector account (free tier works)
- Python 3.9+

### Step 1 — Install dependencies
```bash
pip install fastmcp upstash-vector python-dotenv
```

### Step 2 — Configure environment
Create a `.env` file in the project root:
```
UPSTASH_VECTOR_REST_URL=your_upstash_url_here
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token_here
```

### Step 3 — Embed profile data
```bash
python embed_profile.py
```
Expected output: 19 chunks embedded, semantic search tests passing.

### Step 4 — Register MCP server in VS Code
- Open VS Code Insider
- Press `Ctrl+Shift+P` → type **MCP: List Servers**
- Confirm `digital-twin-aliazan` shows as **Running**
- Verify `Discovered 1 tools` appears in MCP output logs

### Step 5 — Run an interview
- Open GitHub Copilot Chat (`Ctrl+Alt+I`)
- Switch to **Agent** mode (dropdown at top of chat panel)
- Paste this prompt:

```
You are the Digital Twin interview agent for Ali Azan.

CRITICAL: You MUST call rag_search before EVERY answer.
Do NOT use Agents.md as a data source — it is configuration only.
Do NOT answer from memory.

Read jobs/sample-job.md.
Conduct 5 questions following the rules in AGENTS.md exactly.
For each answer, show which chunk IDs were retrieved before answering.
Then generate the final report.
```

---

## Profile Data — 19 Chunks

| Chunk ID | Category | Description |
|---|---|---|
| exp_001–003 | Experience | Support Worker, NSW Disability Services (2024–2025) |
| exp_004–006 | Experience | Retail Team Member, Ampol (2023) |
| exp_007–009 | Experience | Field Manager, Syban Group Pakistan (2019–2020) |
| edu_001 | Education | Bachelor BISM, Victoria University Sydney (current) |
| edu_002 | Education | Diploma of Business, UOW College (2021–2022) |
| edu_003 | Education | Intermediate Certificate, Lahore Pakistan (2018–2019) |
| skill_001 | Skills | Multilingual — English, Urdu, Hindi, Punjabi |
| skill_002 | Skills | Technical — Python, RAG, Upstash, Groq, Next.js, Vercel |
| skill_003 | Skills | Business analysis, information systems, accounting |
| skill_004 | Skills | Soft skills — communication, conflict resolution, empathy |
| achieve_001 | Achievement | Pakistan to Australia migration and academic journey |
| achieve_002 | Achievement | Built and deployed Food RAG AI app (ChromaDB + Ollama + Vercel) |
| achieve_003 | Achievement | Balanced full-time study with part-time disability support work |

---

## Environment Variables

```
UPSTASH_VECTOR_REST_URL      Your Upstash Vector REST endpoint
UPSTASH_VECTOR_REST_TOKEN    Your Upstash Vector token
```

> ⚠️ Never commit `.env` to GitHub. It is listed in `.gitignore`.

---

## Test Results

| Metric | Result |
|---|---|
| MCP Server Status | ✅ Running |
| Tools Discovered | ✅ 1 (rag_search) |
| Chunks Embedded | ✅ 19 / 19 |
| Interview Score | ✅ 86% |
| Pass/Fail Decision | ✅ STRONG PASS |
| RAG calls per answer | ✅ Every question |
| Chunk IDs cited | ✅ Yes (exp_002, skill_003, etc.) |

---

## Related Projects

- Week 2 Food RAG: https://github.com/aliazansaroya786/ragfood
- Week 4 Web App: https://github.com/aliazansaroya786/v0-food-rag-web-app