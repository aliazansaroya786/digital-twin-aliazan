# 🤖 Digital Twin — Ali Azan

> An AI-powered Digital Twin that conducts professional job interviews autonomously using RAG (Retrieval-Augmented Generation) with real career evidence stored in Upstash Vector Database.

---

## 👤 About

**Student:** Ali Azan  
**Course:** Bachelor of Business Information Systems Management (Minor in Accounting)  
**University:** Victoria University, Sydney NSW  
**Email:** aliazansaroya786@gmail.com

---

## 🌐 Live Demo

🔗 **Web Application:** [Add Vercel URL after deployment]  
🔗 **GitHub Repository:** https://github.com/aliazansaroya786/digital-twin-aliazan

---

## 🏗️ System Architecture

```
Job Description Input
        ↓
Interview Agent (Groq llama-3.3-70b)
        ↓
RAG Search Tool (rag_search)
        ↓
Upstash Vector Database
(Ali Azan's 20 career profile chunks)
        ↓
Retrieved Evidence
        ↓
STAR Format Answer
        ↓
Score + Pass/Fail Report
```

---

## 🚀 Development Journey

```
WEEK 1 — Foundation
──────────────────
GitHub repo, README, PRD, agents.md, ClickUp

WEEK 2 — Data & Embeddings
──────────────────────────
profile.json (20 chunks), embed_profile.py
Upstash Vector DB, design.md

WEEK 3 — Interview Agent
─────────────────────────
mcp_server.py (RAG tool)
interview_agent.py (Python CLI)
Autonomous interview + report generation

WEEK 4 — Web Interface
───────────────────────
v0.dev Next.js web app
Vercel deployment
Live interview UI

WEEK 5 — Polish & Analytics
────────────────────────────
Enhanced data quality
Analytics dashboard
Performance metrics

WEEK 6 — Final Presentation
────────────────────────────
Demo video
Final documentation
Presentation slides
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Vector Database | Upstash Vector (bge-large-en-v1.5) |
| LLM | Groq llama-3.3-70b-versatile |
| Python Agent | Python 3.9+ |
| Web Frontend | Next.js 15, TypeScript, Shadcn UI |
| Deployment | Vercel |
| Project Management | ClickUp |

---

## 📁 Repository Structure

```
digital-twin-aliazan/
├── agents.md                     # Agent behaviour instructions
├── README.md                     # This file
├── embed_profile.py              # Upload career data to Upstash
├── mcp_server.py                 # RAG search tool
├── interview_agent.py            # Python CLI interview agent
├── v0_prompt.md                  # Prompt to build web interface
├── .env.example                  # Environment variables template
├── .gitignore
├── data/
│   └── profile.json              # Ali Azan's career profile (20 chunks)
├── jobs/
│   └── sample-job.md             # Sample job descriptions
├── reports/                      # Generated interview reports (auto-created)
└── docs/
    ├── prd.md                    # Product Requirements Document
    ├── design.md                 # Technical Design
    └── implementation-plan.md   # Week by week plan
```

---

## 💻 Getting Started

### Prerequisites
```
Python 3.9+
pip install upstash-vector groq python-dotenv
```

### Setup
```bash
# Clone repo
git clone https://github.com/aliazansaroya786/digital-twin-aliazan.git
cd digital-twin-aliazan

# Install dependencies
pip install upstash-vector groq python-dotenv

# Configure credentials
cp .env.example .env
# Edit .env with your credentials

# Upload career data to Upstash
python embed_profile.py

# Test RAG search tool
python mcp_server.py

# Run Python CLI interview
python interview_agent.py
```

---

## 🔑 Environment Variables

```env
UPSTASH_VECTOR_REST_URL=your_url
UPSTASH_VECTOR_REST_TOKEN=your_token
GROQ_API_KEY=your_groq_key
```

---

## 🎯 How to Run an Interview

### Option 1 — Python CLI
```bash
python interview_agent.py
# Paste job description when prompted
# Type END when done
# Interview runs automatically
# Report saved to reports/ folder
```

### Option 2 — Web Interface
```
Visit the live Vercel URL
Select interviewer role
Paste job description
Click Start Interview
Watch autonomous interview
See pass/fail result
```

---

## 📊 Interview Report Sample

```
# Interview Report — Ali Azan
Date: 2026-04-23
Score: 82%
Decision: PASS ✅

Q1: Tell me about a time you worked with diverse communities...
Evidence: Support Worker at NSW Disability Services
Answer: In my role as Support Worker...
Score: 8/10

Recommendation: Ali Azan demonstrates strong community engagement
skills and relevant experience for this role...
```

---

## 🔗 Documentation

- [Product Requirements](docs/prd.md)
- [Technical Design](docs/design.md)
- [Implementation Plan](docs/implementation-plan.md)
- [Agent Instructions](agents.md)
- [v0.dev Web Prompt](v0_prompt.md)