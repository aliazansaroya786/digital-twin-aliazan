"""
MCP Server - Digital Twin Ali Azan
Exposes rag_search() tool to VS Code Agent Mode (GitHub Copilot)
"""

import os
import sys
import json
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from upstash_vector import Index

# Fix Windows Unicode encoding
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

load_dotenv()

# Upstash Vector setup
index = Index(
    url=os.environ["UPSTASH_VECTOR_REST_URL"],
    token=os.environ["UPSTASH_VECTOR_REST_TOKEN"],
)

# MCP Server
mcp = FastMCP("digital-twin-aliazan")


@mcp.tool()
def rag_search(query: str, top_k: int = 3) -> str:
    """
    Search Ali Azan's career profile vector database.

    Use this tool before answering ANY interview question.
    Returns the most relevant career evidence for the given query.

    Args:
        query: The interview question or relevant keywords to search for.
        top_k: Number of results to return (default 3, max 5).

    Returns:
        JSON string with retrieved career evidence, scores, and metadata.
    """
    top_k = min(top_k, 5)

    try:
        results = index.query(data=query, top_k=top_k, include_metadata=True)
    except Exception as e:
        return json.dumps({"error": str(e), "results": []})

    if not results:
        return json.dumps({
            "message": "No relevant evidence found for this query.",
            "results": []
        })

    output = []
    for r in results:
        output.append({
            "id": r.id,
            "score": round(r.score, 4),
            "text": r.metadata.get("text", ""),
            "category": r.metadata.get("category", ""),
            "role": r.metadata.get("role", ""),
            "organization": r.metadata.get("organization", ""),
            "skills": r.metadata.get("skills", ""),
            "type": r.metadata.get("type", ""),
        })

    return json.dumps({"results": output}, indent=2)


# Entry point
if __name__ == "__main__":
    print("Digital Twin MCP Server starting...")
    print("rag_search() tool registered and ready.")
    mcp.run(transport="stdio")