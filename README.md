# 🤖 Digital Twin — Ali Azan

> An AI-powered Digital Twin built on RAG (Retrieval-Augmented Generation) that can conduct professional interviews on behalf of Ali Azan using real career data stored in a vector database.

---

## 👤 About

**Student:** Ali Azan  
**Course:** Bachelor of Business Information Systems Management (Minor in Accounting)  
**University:** Victoria University, Sydney NSW  
**Project:** AI Data Analyst Industry Project — Digital Twin  

---

## 🎯 Project Overview

This Digital Twin is a structured, AI-powered representation of Ali Azan's professional capability. When an AI agent asks interview questions, it retrieves real evidence from Ali Azan's career history stored in Upstash Vector Database and responds accurately on his behalf.

---

## 🏗️ Architecture

```
Job Description Input
        ↓
Agentic LLM (Claude / Groq)
        ↓
MCP Tool Call → RAG Search
        ↓
Upstash Vector Database
        ↓
Retrieved Career Evidence
        ↓
Grounded Interview Answer
        ↓
Pass/Fail Recommendation Report
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Vector Database | Upstash Vector |
| Embedding Model | bge-large-en-v1.5 |
| LLM | Claude Sonnet / Groq |
| Agent Mode | VS Code Insider + GitHub Copilot |
| Project Management | ClickUp |
| Version Control | GitHub |

---

## 📁 Repository Structure

```
digital-twin-aliazan/
├── agents.md                    # Agent instructions and behaviour rules
├── README.md                    # Project overview (this file)
├── docs/
│   ├── prd.md                   # Product Requirements Document
│   ├── design.md                # Technical Design Document
│   └── implementation-plan.md  # Implementation Plan
├── data/
│   └── profile.json             # Ali Azan's career data (submitted separately)
├── jobs/
│   └── sample-job.md            # Sample job descriptions for interviews
└── .env.example                 # Environment variables template
```

---

## 🚀 Getting Started

### Prerequisites
- VS Code Insider Edition
- GitHub Copilot Pro
- Upstash Vector account
- Python 3.9+

### Setup
```bash
# Clone repository
git clone https://github.com/aliazansaroya786/digital-twin-aliazan.git
cd digital-twin-aliazan

# Install dependencies
pip install upstash-vector groq python-dotenv

# Configure environment
cp .env.example .env
# Fill in your credentials

# Run embedding pipeline
python embed_profile.py

# Start interview agent
# Open VS Code Insider → Agent Mode → "Commence the interview"
```

---

## 🔑 Environment Variables

```env
UPSTASH_VECTOR_REST_URL
UPSTASH_VECTOR_REST_TOKEN
GROQ_API_KEY
```

---

## 📖 Documentation

- [Product Requirements Document](docs/prd.md)
- [Technical Design](docs/design.md)
- [Implementation Plan](docs/implementation-plan.md)
- [Agent Instructions](agents.md)

---

## 🔗 Related Projects

- **Week 2 Food RAG:** https://github.com/aliazansaroya786/ragfood
- **Week 4 Web App:** https://github.com/aliazansaroya786/v0-food-rag-web-app