# Technical Design Document
## Digital Twin — Ali Azan

**Version:** 1.0  
**Generated with:** Claude AI (Anthropic)  
**Based on:** docs/prd.md  
**Date:** April 2026

---

## 1. System Architecture

```
┌─────────────────────────────────────────┐
│           INPUT LAYER                    │
│  Job Description + Interview Command     │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│           AGENT LAYER                    │
│  Claude Sonnet 4.5 / Groq LLM           │
│  (VS Code Agent Mode + GitHub Copilot)  │
└─────────────────┬───────────────────────┘
                  ↓ MCP Tool Call
┌─────────────────────────────────────────┐
│           RAG LAYER                      │
│  rag_search() MCP Tool                  │
│  Semantic query → vector similarity     │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│           STORAGE LAYER                  │
│  Upstash Vector Database                │
│  bge-large-en-v1.5 embeddings           │
│  Ali Azan's career profile chunks       │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│           OUTPUT LAYER                   │
│  Interview Transcript                   │
│  Pass/Fail Report (Markdown)            │
└─────────────────────────────────────────┘
```

---

## 2. Data Design

### 2.1 Profile JSON Structure

```json
{
  "id": "unique_chunk_id",
  "category": "experience|education|skills|achievement",
  "text": "Detailed description of the career fact (75+ words)",
  "metadata": {
    "role": "Job title or context",
    "organization": "Company or institution name",
    "location": "City, State, Country",
    "date_start": "YYYY-MM",
    "date_end": "YYYY-MM or present",
    "skills": ["skill1", "skill2"],
    "type": "work|education|skill|achievement"
  }
}
```

### 2.2 Data Categories

| Category | Description | Minimum Chunks |
|----------|-------------|----------------|
| Education | Degrees, courses, institutions | 4 chunks |
| Experience | Work history with STAR examples | 9 chunks |
| Skills | Technical and soft skills | 4 chunks |
| Achievements | Key accomplishments | 3 chunks |
| **Total** | | **20+ chunks** |

### 2.3 Sample Data Chunks

```json
[
  {
    "id": "exp_001",
    "category": "experience",
    "text": "As a Support Worker at NSW Disability and Community Service from September 2024 to April 2025 in Marrickville NSW, Ali Azan facilitated community participation initiatives and daily activity planning. He enabled clients to engage confidently in social, recreational, and skill-building programmes tailored to individual goals. This role required strong empathy, communication, and organizational skills to support people with disabilities.",
    "metadata": {
      "role": "Support Worker",
      "organization": "NSW Disability and Community Service",
      "location": "Marrickville, NSW",
      "date_start": "2024-09",
      "date_end": "2025-04",
      "skills": ["community support", "communication", "planning", "advocacy"],
      "type": "work"
    }
  },
  {
    "id": "edu_001",
    "category": "education",
    "text": "Ali Azan is currently completing a Bachelor of Business Information Systems Management with a Minor in Accounting at Victoria University in Sydney NSW. This degree combines technology and business knowledge, covering information systems, data analysis, database management, business intelligence, and accounting fundamentals. This education provides strong foundation for roles in IT, data analysis, and business systems.",
    "metadata": {
      "role": "Student",
      "organization": "Victoria University",
      "location": "Sydney, NSW",
      "date_start": "2022-01",
      "date_end": "present",
      "skills": ["information systems", "data analysis", "accounting", "business intelligence"],
      "type": "education"
    }
  }
]
```

---

## 3. Embedding Pipeline Design

### 3.1 Process Flow

```
profile.json
     ↓
Load and validate chunks
     ↓
For each chunk:
  - Combine text + metadata for enriched embedding
  - Send to Upstash Vector (auto-embedding)
  - Store with metadata
     ↓
Verify all chunks stored
     ↓
Test semantic search
```

### 3.2 Embedding Script

```python
from upstash_vector import Index
import json
import os
from dotenv import load_dotenv

load_dotenv()

index = Index(
    url=os.environ.get("UPSTASH_VECTOR_REST_URL"),
    token=os.environ.get("UPSTASH_VECTOR_REST_TOKEN")
)

with open("data/profile.json", "r") as f:
    chunks = json.load(f)

for chunk in chunks:
    enriched_text = f"{chunk['text']} Role: {chunk['metadata']['role']}. Skills: {', '.join(chunk['metadata']['skills'])}."
    index.upsert(vectors=[{
        "id": chunk["id"],
        "data": enriched_text,
        "metadata": chunk["metadata"]
    }])
    print(f"✅ Embedded: {chunk['id']}")

print(f"✅ Total embedded: {len(chunks)} chunks")
```

---

## 4. MCP Tool Design

### 4.1 RAG Search Tool

```python
def rag_search(query: str, top_k: int = 3) -> list:
    """
    MCP Tool: Search Ali Azan's career profile
    Called by agent before every interview answer
    """
    results = index.query(
        data=query,
        top_k=top_k,
        include_metadata=True
    )
    
    return [
        {
            "text": r.metadata.get("text", ""),
            "score": r.score,
            "role": r.metadata.get("role", ""),
            "category": r.metadata.get("category", "")
        }
        for r in results
    ]
```

---

## 5. Agent Design

### 5.1 System Prompt

```
You are conducting a professional job interview for Ali Azan.
For every question, you MUST call rag_search() first.
Answer only using retrieved evidence.
Use STAR format for behavioural questions.
Score each answer out of 10.
Generate a final pass/fail report.
```

### 5.2 Interview Flow

```
1. Read job description
2. Generate 5-8 tailored questions
3. For each question:
   a. Call rag_search(question_keywords)
   b. Review retrieved evidence
   c. Construct STAR answer
   d. Score the answer
4. Calculate overall score
5. Generate Markdown report
6. Output pass/fail decision
```

---

## 6. Security Design

```
✅ .env for all credentials
✅ .gitignore excludes .env and profile data
✅ No personal data in GitHub
✅ Public repo contains only code, not data
✅ Data submitted separately via LMS
```

---

## 7. Testing Strategy

| Test | Method | Expected Result |
|------|--------|----------------|
| Embedding pipeline | Run embed_profile.py | 20+ vectors in Upstash |
| Semantic search | Query with job keywords | Relevant chunks returned |
| Agent interview | Run full interview | Complete Q&A transcript |
| Report generation | Check output file | Markdown report with score |
| Security | Check GitHub | No secrets visible |