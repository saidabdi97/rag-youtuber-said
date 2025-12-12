import google.generativeai as genai
from dotenv import load_dotenv
import os
import lancedb
from pathlib import Path

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

genai.configure(api_key=GOOGLE_API_KEY)

# -------------------------------------------------
# Embedding model setup (same as ingestion)
# -------------------------------------------------
embedding_model = "models/text-embedding-004"

def embed_query(query: str):
    """Embed a user query using the same embedding model."""
    result = genai.embed_content(
        model=embedding_model,
        content=query,
        task_type="retrieval_query"
    )
    return result["embedding"]

# -------------------------------------------------
# Connect LanceDB & load table
# -------------------------------------------------
db_path = "lancedb"
db = lancedb.connect(db_path)
table_name = "transcripts"

if table_name not in db.table_names():
    raise ValueError("❌ LanceDB table not found. Run ingestion first.")

table = db.open_table(table_name)

# -------------------------------------------------
# Retrieval function
# -------------------------------------------------
def retrieve_relevant_docs(query: str, k: int = 5):
    """Return the top-k most relevant documents for a user query."""
    query_embedding = embed_query(query)

    # Vector search
    results = table.search(query_embedding).limit(k).to_list()

    # Format output
    docs = [
        {
            "filename": r["filename"],
            "text": r["text"]
        }
        for r in results
    ]

    return docs

# -------------------------------------------------
# Test block
# -------------------------------------------------
if __name__ == "__main__":
    print("🔍 Testing retrieval...")

    test_query = "Vad handlar logistic regression om?"
    docs = retrieve_relevant_docs(test_query, k=3)

    print(f"Antal dokument hittade: {len(docs)}")
    for i, d in enumerate(docs, start=1):
        print(f"\n--- Dokument {i} ---")
        print("Fil:", d["filename"])
        print("Text (första 200 tecken):")
        print(d["text"][:200])
