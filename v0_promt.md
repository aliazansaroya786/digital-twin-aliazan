# v0.dev Prompt — Digital Twin Web Interface

Copy and paste this entire prompt into v0.dev to build the web interface.

---

## PROMPT TO PASTE INTO v0.dev:

Build a professional Digital Twin Interview Web Application using Next.js 15, TypeScript, Server Actions, and Shadcn UI.

## What This App Does:
A recruiter visits the website, pastes a job description, clicks Start Interview, and watches an AI autonomously interview a candidate called "Ali Azan" using RAG (Retrieval-Augmented Generation) from Upstash Vector Database. The AI retrieves real career evidence and generates grounded answers. At the end it shows a pass/fail hiring recommendation.

## Tech Stack:
- Next.js 15 with App Router
- TypeScript
- Shadcn UI components
- Tailwind CSS
- Upstash Vector SDK (@upstash/vector)
- Groq SDK (groq)

## Environment Variables Needed:
- UPSTASH_VECTOR_REST_URL
- UPSTASH_VECTOR_REST_TOKEN  
- GROQ_API_KEY

## Pages Required:

### Page 1: Home / Interview Setup (/)
- Professional header: "Digital Twin — Ali Azan"
- Subtitle: "AI-Powered Interview Agent"
- Interviewer role dropdown: Recruiter / Hiring Manager / Custom
- Large textarea: "Paste Job Description Here"
- "Start Interview" button (prominent, blue)
- "Example Queries" section showing 3 sample job descriptions
- Clean, professional dark theme

### Page 2: Live Interview (/interview)
- Show candidate name: Ali Azan
- Show job title being interviewed for
- Questions appear one by one as they are generated
- For each question show:
  - The question text
  - "🔍 Searching profile..." loading state
  - Retrieved evidence sources (collapsed/expandable)
  - The AI-generated answer in STAR format
  - Score out of 10
- Progress bar showing interview progress
- Real-time streaming of answers

### Page 3: Report (/report)
- Large score display (e.g., "82%")
- PASS ✅ or FAIL ❌ badge (pass = 70%+)
- Full interview transcript
- Hiring recommendation paragraph
- Download Report as PDF button
- Start New Interview button

## Server Actions Required:

### action: generateQuestions(jobDescription)
```typescript
// Call Groq to generate 6 interview questions
// Return array of question strings
```

### action: answerQuestion(question, jobDescription)
```typescript
// 1. Search Upstash Vector with the question
// 2. Get top 3 results as evidence
// 3. Call Groq with evidence to generate STAR answer
// 4. Score the answer 1-10
// 5. Return { answer, evidence, score }
```

### action: generateReport(jobDescription, results)
```typescript
// Calculate overall score and percentage
// Generate hiring recommendation using Groq
// Return markdown report string
// Pass if score >= 70%
```

## Upstash Vector Search Code:
```typescript
import { Index } from "@upstash/vector";

const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL!,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
});

const results = await index.query({
  data: question,
  topK: 3,
  includeMetadata: true,
});
```

## Groq LLM Code:
```typescript
import Groq from "groq-sdk";

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

const response = await groq.chat.completions.create({
  model: "llama-3.3-70b-versatile",
  messages: [{ role: "user", content: prompt }],
  max_tokens: 400,
});
```

## Design Requirements:
- Dark professional theme (navy/dark background)
- Clean card-based layout
- Smooth animations when questions appear
- Mobile responsive
- Loading spinners during API calls
- Error handling with user-friendly messages
- Professional typography

## Candidate Profile Summary (for system prompt):
Ali Azan is a Bachelor of Business Information Systems Management student at Victoria University Sydney. He has worked as a Support Worker at NSW Disability Services (2024-2025), Retail Team Member at Ampol (2023), and Field Manager at Syban Group Pakistan (2019-2020). He is fluent in English, Urdu, Hindi, and Punjabi. His skills include Python, AI/RAG systems, data analysis, customer service, community support, and team management.

## Important:
- All answers MUST come from Upstash Vector search results
- Never hallucinate facts about Ali Azan
- Show retrieved evidence sources for transparency
- Minimum 70% score required to PASS