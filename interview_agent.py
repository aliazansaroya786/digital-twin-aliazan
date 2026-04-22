import os
import json
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from upstash_vector import Index

load_dotenv()

# Setup clients
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
index = Index(
    url=os.environ.get("UPSTASH_VECTOR_REST_URL"),
    token=os.environ.get("UPSTASH_VECTOR_REST_TOKEN")
)

CANDIDATE_NAME = "Ali Azan"
LLM_MODEL = "llama-3.3-70b-versatile"

def rag_search(query: str, top_k: int = 3) -> list:
    """Search Ali Azan's career profile"""
    try:
        results = index.query(data=query, top_k=top_k, include_metadata=True)
        return [
            {
                "id": r.id,
                "score": round(r.score, 4),
                "text": r.metadata.get("text", "") if r.metadata else "",
                "role": r.metadata.get("role", "") if r.metadata else "",
                "organization": r.metadata.get("organization", "") if r.metadata else "",
            }
            for r in results
        ]
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []


def format_evidence(results: list) -> str:
    """Format retrieved evidence"""
    if not results:
        return "No relevant evidence found in profile database."
    parts = []
    for i, r in enumerate(results, 1):
        parts.append(
            f"[Evidence {i}] (Score: {r['score']}) "
            f"{r['role']} at {r['organization']}\n{r['text']}"
        )
    return "\n\n".join(parts)


def generate_questions(job_description: str) -> list:
    """Generate interview questions based on job description"""
    print("\n🤖 Generating interview questions...\n")
    
    prompt = f"""You are a professional interviewer. Based on this job description, 
generate exactly 6 interview questions for candidate {CANDIDATE_NAME}.

Mix of question types:
- 2 behavioural questions (Tell me about a time...)
- 2 technical/skills questions
- 1 situational question
- 1 motivational question

Job Description:
{job_description}

Return ONLY a JSON array of 6 question strings, nothing else.
Example: ["Question 1?", "Question 2?", ...]"""

    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    text = response.choices[0].message.content.strip()
    # Clean JSON
    if "```" in text:
        text = text.split("```")[1].replace("json", "").strip()
    
    questions = json.loads(text)
    return questions


def answer_question(question: str, job_description: str) -> dict:
    """Answer a single interview question using RAG"""
    
    # Step 1: Search for relevant evidence
    print(f"  🔍 Searching profile for: '{question[:50]}...'")
    results = rag_search(question, top_k=3)
    evidence = format_evidence(results)
    
    # Step 2: Generate answer using evidence
    prompt = f"""You are {CANDIDATE_NAME}, a professional candidate being interviewed.
Answer this interview question using ONLY the evidence provided below.
Use STAR format (Situation, Task, Action, Result) for behavioural questions.
Speak in first person. Be professional and specific.
If evidence is not relevant, say you don't have direct experience but relate what you do have.

Job Description Context:
{job_description[:500]}

Evidence from your career profile:
{evidence}

Interview Question: {question}

Answer (2-3 paragraphs maximum):"""

    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    
    answer = response.choices[0].message.content.strip()
    
    # Step 3: Score the answer
    score_prompt = f"""Rate this interview answer from 1-10 based on:
- Relevance to the question (40%)
- Use of specific evidence (40%)  
- Communication clarity (20%)

Question: {question}
Answer: {answer}

Return ONLY a number between 1-10, nothing else."""

    score_response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": score_prompt}],
        max_tokens=5
    )
    
    try:
        score = int(score_response.choices[0].message.content.strip())
        score = max(1, min(10, score))
    except:
        score = 7
    
    return {
        "question": question,
        "evidence": results,
        "answer": answer,
        "score": score
    }


def generate_report(job_description: str, interview_results: list) -> str:
    """Generate final interview report with pass/fail decision"""
    
    total_score = sum(r["score"] for r in interview_results)
    avg_score = round(total_score / len(interview_results), 1)
    percentage = round((avg_score / 10) * 100)
    decision = "PASS ✅" if percentage >= 70 else "FAIL ❌"
    
    # Generate recommendation
    rec_prompt = f"""Write a professional hiring recommendation for {CANDIDATE_NAME}.
Candidate scored {percentage}% ({avg_score}/10 average).
Decision: {"PASS" if percentage >= 70 else "FAIL"}

Job: {job_description[:300]}

Write 2-3 sentences explaining the recommendation based on the score.
Be professional and specific."""

    rec_response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": rec_prompt}],
        max_tokens=200
    )
    recommendation = rec_response.choices[0].message.content.strip()
    
    # Build report
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"""# 📋 Interview Report — {CANDIDATE_NAME}

**Date:** {now}  
**Overall Score:** {percentage}%  
**Average:** {avg_score}/10  
**Decision:** {decision}  

---

## 💼 Job Description
{job_description[:500]}

---

## 📝 Interview Transcript

"""
    for i, result in enumerate(interview_results, 1):
        report += f"""### Q{i}: {result['question']}

**🔍 Evidence Retrieved:**
"""
        for j, ev in enumerate(result['evidence'], 1):
            report += f"- [{j}] {ev['role']} at {ev['organization']} (score: {ev['score']})\n"
        
        report += f"""
**💬 Answer:**
{result['answer']}

**⭐ Score:** {result['score']}/10

---

"""

    report += f"""## 🏆 Hiring Recommendation

**Decision: {decision}**  
**Score: {percentage}%**

{recommendation}

---
*Report generated by Digital Twin AI Agent — {CANDIDATE_NAME}*
"""
    return report, percentage


def run_interview(job_description: str):
    """Run a complete autonomous interview"""
    
    print(f"\n{'='*60}")
    print(f"🤖 DIGITAL TWIN INTERVIEW AGENT")
    print(f"Candidate: {CANDIDATE_NAME}")
    print(f"{'='*60}\n")
    
    # Generate questions
    questions = generate_questions(job_description)
    print(f"✅ Generated {len(questions)} interview questions\n")
    
    # Answer each question
    interview_results = []
    for i, question in enumerate(questions, 1):
        print(f"\n{'─'*50}")
        print(f"Q{i}: {question}")
        print(f"{'─'*50}")
        
        result = answer_question(question, job_description)
        interview_results.append(result)
        
        print(f"\n💬 Answer:")
        print(result["answer"])
        print(f"\n⭐ Score: {result['score']}/10")
    
    # Generate report
    print(f"\n\n{'='*60}")
    print("📊 Generating final report...")
    report, percentage = generate_report(job_description, interview_results)
    
    # Save report
    filename = f"interview_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{filename}", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n{'='*60}")
    print(f"✅ Interview Complete!")
    print(f"📊 Final Score: {percentage}%")
    print(f"{'✅ PASS' if percentage >= 70 else '❌ FAIL'}")
    print(f"📄 Report saved: reports/{filename}")
    print(f"{'='*60}\n")
    
    return report, percentage


if __name__ == "__main__":
    print("🤖 Digital Twin Interview Agent")
    print("="*60)
    print("\nPaste the job description below.")
    print("When done, type 'END' on a new line and press Enter:\n")
    
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    
    job_description = "\n".join(lines)
    
    if not job_description.strip():
        # Use sample job for testing
        job_description = """
        Data Analyst — Victoria University
        We are looking for a motivated Data Analyst with strong analytical skills.
        Requirements:
        - Experience with data analysis and reporting
        - Strong communication skills
        - Ability to work in a team
        - Knowledge of information systems
        - Customer service experience preferred
        """
        print("⚠️  No input provided. Using sample job description.")
    
    run_interview(job_description)