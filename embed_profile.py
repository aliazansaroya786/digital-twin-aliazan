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

# Load profile data
with open("data/profile.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Check existing
info = index.info()
print(f"📊 Existing vectors: {info.vector_count}")

if True:  # Always re-embed for testing
    print(f"\n🔄 Re-embedding {len(chunks)} profile chunks...")
    
    for i, chunk in enumerate(chunks):
        index.upsert(vectors=[{
            "id": chunk["id"],
            "data": f"{chunk['text']} {', '.join(chunk['metadata']['skills'])}",
            "metadata": {
                "text": chunk["text"],
                "category": chunk["category"],
                "role": chunk["metadata"]["role"],
                "organization": chunk["metadata"]["organization"],
                "skills": ", ".join(chunk["metadata"]["skills"]),
                "type": chunk["metadata"]["type"]
            }
        }])
        print(f"  ✅ ({i+1}/{len(chunks)}) Embedded: {chunk['id']}")
    
    print(f"\n✅ All {len(chunks)} chunks re-embedded successfully!")
else:
    print(f"✅ Already have {info.vector_count} vectors. Skipping.")

# Test search
print("\n🔍 Testing semantic search...")
test_queries = [
    "community support disability",
    "retail customer service",
    "leadership management",
    "technical AI skills",
    "education university"
]

for query in test_queries:
    results = index.query(data=query, top_k=1, include_metadata=True)
    if results:
        print(f"Query: '{query}' → Best match: {results[0].id} (score: {round(results[0].score, 4)})")

print("\n✅ Digital Twin is ready for interviews!")