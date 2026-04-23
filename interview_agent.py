import os
import json
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from upstash_vector import Index

load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
index = Index(
    url=os.environ.get("UPSTASH_VECTOR_REST_URL"),
    token=os.environ.get("UPSTASH_VECTOR_REST_TOKEN")
)

CANDIDATE_NAME = "Ali Azan"
LLM_MODEL = "llama-3.3-70b-versatile"


def rag_search(query: str, top_k: int = 3) -> list:
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
        print(f"Search error: {e}")
        return []


def format_evidence(results: list) -> str:
    if not results:
        return "No relevant evidence found."
    parts = []
    for i, r in enumerate(results, 1):
        parts.append(f"[Source {i}] {r['role']} at {r['organization']}\n{r['text']}")
    return "\n\n".join(parts)


def generate_questions(job_description: str) -> list:
    print("\n Generating interview questions...\n")
    prompt = f"""Generate exactly 6 interview questions for {CANDIDATE_NAME} based on this job:
{job_description}
Mix: 2 behavioural, 2 technical, 1 situational, 1 motivational.
Return ONLY a JSON array: ["Q1?", "Q2?", ...]"""

    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    text = response.choices[0].message.content.strip()
    if "```" in text:
        text = text.split("```")[1].replace("json", "").strip()
    try:
        return json.loads(text)
    except:
        return [
            "Tell me about yourself.",
            "Describe a time you worked with diverse communities.",
            "What technical skills do you bring?",
            "How do you handle challenging situations?",
            "Where do you see yourself in 5 years?",
            "Why are you interested in this position?"
        ]


def answer_question(question: str, job_description: str) -> dict:
    results = rag_search(question, top_k=3)
    evidence = format_evidence(results)

    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": f"""You are {CANDIDATE_NAME} being interviewed.
Answer using ONLY this evidence. Use STAR format. Speak in first person.
Job: {job_description[:200]}
Evidence: {evidence}
Question: {question}
Answer:"""}],
        max_tokens=400
    )
    answer = response.choices[0].message.content.strip()

    score_res = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": f"Rate 1-10. Return ONLY a number.\nQ:{question}\nA:{answer}"}],
        max_tokens=5
    )
    try:
        score = int(score_res.choices[0].message.content.strip())
        score = max(1, min(10, score))
    except:
        score = 7

    return {"question": question, "evidence": results, "answer": answer, "score": score}


def generate_report(job_description: str, results: list) -> tuple:
    avg = sum(r["score"] for r in results) / len(results)
    percentage = round((avg / 10) * 100)
    decision = "PASS" if percentage >= 70 else "FAIL"

    rec = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": f"2 sentence hiring recommendation for {CANDIDATE_NAME}. Score:{percentage}%. Decision:{decision}. Job:{job_description[:150]}"}],
        max_tokens=150
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"# Interview Report — {CANDIDATE_NAME}\n\n"
    report += f"**Date:** {now}\n**Score:** {percentage}%\n**Decision:** {'PASS' if percentage >= 70 else 'FAIL'}\n\n---\n\n"
    report += f"## Job\n{job_description[:300]}\n\n---\n\n## Transcript\n\n"

    for i, r in enumerate(results, 1):
        report += f"### Q{i}: {r['question']}\n"
        for j, ev in enumerate(r['evidence'], 1):
            report += f"- Source {j}: {ev['role']} at {ev['organization']} ({ev['score']})\n"
        report += f"\n**Answer:** {r['answer']}\n**Score:** {r['score']}/10\n\n---\n\n"

    report += f"## Recommendation\n**{decision}** — {percentage}%\n\n{rec.choices[0].message.content}\n"
    return report, percentage


def chat_mode():
    print(f"\n{'='*60}")
    print("FREE CHAT MODE — Ask Anything About Ali Azan")
    print("Type 'exit' to quit")
    print(f"{'='*60}\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        if not question:
            continue

        print("Searching profile...")
        results = rag_search(question, top_k=3)
        evidence = format_evidence(results)

        response = groq_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": f"You represent {CANDIDATE_NAME}'s profile. Answer using ONLY the evidence. Be professional. Say '{CANDIDATE_NAME}' or 'he/him'."},
                {"role": "user", "content": f"Evidence:\n{evidence}\n\nQuestion: {question}\n\nAnswer:"}
            ],
            max_tokens=400
        )

        print(f"\nAli Azan's Twin: {response.choices[0].message.content.strip()}")
        print(f"\nSources:")
        for i, r in enumerate(results, 1):
            print(f"  [{i}] {r['role']} at {r['organization']} (score: {r['score']})")
        print()


def run_interview(job_description: str):
    print(f"\n{'='*60}")
    print(f"DIGITAL TWIN — {CANDIDATE_NAME}")
    print(f"{'='*60}\n")
    print("PART 1: AUTOMATED INTERVIEW")
    print("─"*60)

    questions = generate_questions(job_description)
    print(f"Generated {len(questions)} questions\n")

    interview_results = []
    for i, question in enumerate(questions, 1):
        print(f"\nQ{i}: {question}")
        print("─"*40)
        result = answer_question(question, job_description)
        interview_results.append(result)
        print(f"Sources: {', '.join([ev['role'] for ev in result['evidence']])}")
        print(f"Answer: {result['answer']}")
        print(f"Score: {result['score']}/10")

    print(f"\n{'='*60}")
    print("Generating report...")
    report, percentage = generate_report(job_description, interview_results)

    os.makedirs("reports", exist_ok=True)
    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Score: {percentage}% — {'PASS' if percentage >= 70 else 'FAIL'}")
    print(f"Report saved: {filename}")
    print(f"{'='*60}")

    print(f"\nInterview done! Entering FREE CHAT MODE...")
    print("Now ask anything about Ali Azan!\n")
    chat_mode()


if __name__ == "__main__":
    print("Digital Twin — Ali Azan")
    print("="*60)
    print("\n1. Full Interview (automated + chat)")
    print("2. Chat Only")
    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "2":
        chat_mode()
    else:
        print("\nPaste job description. Type END when done:\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        job_description = "\n".join(lines)
        if not job_description.strip():
            job_description = "Data Analyst role requiring strong communication, data analysis, and customer service skills."
            print("Using sample job.")

        run_interview(job_description)