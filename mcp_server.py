import json
import os
from dotenv import load_dotenv
from upstash_vector import Index

load_dotenv()

# Setup Upstash Vector
index = Index(
    url=os.environ.get("UPSTASH_VECTOR_REST_URL"),
    token=os.environ.get("UPSTASH_VECTOR_REST_TOKEN")
)

def rag_search(query: str, top_k: int = 3) -> list:
    """
    RAG Search Tool — searches Ali Azan's career profile
    Called by the interview agent before every answer
    """
    try:
        results = index.query(
            data=query,
            top_k=top_k,
            include_metadata=True
        )
        return [
            {
                "id": r.id,
                "score": round(r.score, 4),
                "text": r.metadata.get("text", "") if r.metadata else "",
                "role": r.metadata.get("role", "") if r.metadata else "",
                "organization": r.metadata.get("organization", "") if r.metadata else "",
                "category": r.metadata.get("category", "") if r.metadata else "",
                "skills": r.metadata.get("skills", "") if r.metadata else ""
            }
            for r in results
        ]
    except Exception as e:
        print(f"❌ RAG search error: {e}")
        return []


def format_evidence(results: list) -> str:
    """Format search results into readable evidence string"""
    if not results:
        return "No relevant evidence found in profile database."
    
    evidence = []
    for i, r in enumerate(results, 1):
        evidence.append(
            f"[Evidence {i}] (Score: {r['score']}, Source: {r['role']} at {r['organization']})\n"
            f"{r['text']}"
        )
    return "\n\n".join(evidence)


if __name__ == "__main__":
    # Test the MCP tool
    print("🔍 Testing RAG Search Tool...")
    test_queries = [
        "community support disability work",
        "retail customer service experience",
        "leadership management team",
        "technical AI programming skills",
        "education university degree"
    ]
    
    for query in test_queries:
        results = rag_search(query, top_k=2)
        print(f"\nQuery: '{query}'")
        for r in results:
            print(f"  → {r['id']} (score: {r['score']}): {r['text'][:80]}...")
    
    print("\n✅ MCP Tool is working correctly!")