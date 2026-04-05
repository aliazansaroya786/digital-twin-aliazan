# Product Requirements Document (PRD)
## Digital Twin — Ali Azan

**Version:** 1.0  
**Author:** Ali Azan  
**Date:** April 2026  
**Course:** Bachelor of Business Information Systems Management  
**University:** Victoria University, Sydney NSW

---

## 1. Product Overview

### Purpose
Build an AI-powered Digital Twin of Ali Azan that can conduct professional job interviews autonomously using real career data retrieved from a vector database. The system ensures all answers are grounded in real evidence, not hallucinations.

### Problem Statement
Job seekers often struggle to articulate their experience clearly in interviews. A Digital Twin solves this by creating an always-available, evidence-based AI representative that can answer interview questions accurately using structured career data.

### Goal
When an AI agent is given a job description and asked to interview Ali Azan, it must:
- Retrieve relevant career facts from the vector database
- Answer questions using real evidence
- Generate a pass/fail hiring recommendation report

---

## 2. AI Study Reference URLs

- Upstash Vector Documentation: https://upstash.com/docs/vector
- Groq API Documentation: https://console.groq.com/docs
- VS Code Agent Mode: https://aiagents.ausbizconsulting.com.au/developer-productivity
- Digital Twin Workshop: https://aiagents.ausbizconsulting.com.au/digital-twin-workshop
- Anthropic Claude API: https://docs.anthropic.com
- RAG Architecture Guide: https://python.langchain.com/docs/concepts/rag/

---

## 3. Candidate Profile

### Personal Information
- **Name:** Ali Azan
- **Location:** Blacktown, NSW, Australia
- **Email:** aliazansaroya786@gmail.com
- **LinkedIn:** in/Ali Azan

### Education
- Bachelor of Business Information Systems Management (Minor in Accounting) — Victoria University, Sydney (Current)
- Diploma of Business — University of Wollongong College, 2021-2022
- Intermediate Certificate — Gov. Inter College, Lahore, Pakistan, 2018-2019
- Secondary School — Gov High School, Narang Mandi, Pakistan, 2016-2017

### Work Experience
1. **Support Worker** — NSW Disability and Community Service (Sep 2024 - Apr 2025)
2. **Retail Team Member** — Ampol Marsden Park (Jan 2023 - Oct 2023)
3. **Field Manager** — Syban Group, Pakistan (Sep 2019 - Oct 2020)

### Skills
- Languages: Urdu, Hindi, Punjabi, English
- Technical: Python, RAG systems, Vector databases, AI tools
- Business: Data analysis, Information systems, Accounting fundamentals
- Soft Skills: Client advocacy, team coordination, community engagement

---

## 4. Functional Requirements

### FR1 — Data Storage
- Store Ali Azan's career profile as structured JSON chunks
- Embed all chunks into Upstash Vector Database
- Each chunk must have metadata: category, date, role, skills

### FR2 — Semantic Search
- Agent must retrieve relevant chunks using semantic similarity
- Search must be based on embeddings, not keywords
- Return top 3-5 most relevant results per query

### FR3 — Autonomous Interview
- Agent must autonomously generate interview questions based on job description
- Agent must call RAG tool to retrieve relevant evidence
- Agent must answer questions using retrieved facts only

### FR4 — Report Generation
- System must generate a Markdown interview report
- Report must include: questions, answers, evidence citations
- Report must include pass/fail recommendation with score

### FR5 — Multiple Job Roles
- System must support different job descriptions
- Agent behaviour must adapt to role requirements
- Pass threshold: minimum 70% score

---

## 5. Non-Functional Requirements

### NFR1 — Performance
- Vector search response: under 3 seconds
- Full interview completion: under 5 minutes
- Report generation: under 30 seconds

### NFR2 — Security
- No personal data committed to GitHub
- All credentials stored in .env files
- .gitignore must exclude sensitive files

### NFR3 — Reliability
- System must handle empty vector search results gracefully
- Error messages must be informative and actionable
- Fallback responses when retrieval fails

### NFR4 — Quality
- All answers must be grounded in retrieved evidence
- No hallucinated facts allowed
- Minimum 3 evidence citations per interview answer

---

## 6. Acceptance Criteria

| Criteria | Requirement |
|----------|-------------|
| Vector DB populated | Minimum 15 vectors stored |
| Semantic search works | Returns relevant results with similarity scores |
| Agent runs autonomously | No manual intervention during interview |
| Report generated | Markdown report with pass/fail decision |
| Security | No secrets in GitHub |
| Documentation | README, PRD, design.md, agents.md all present |