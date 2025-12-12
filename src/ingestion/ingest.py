import os
from dotenv import load_dotenv
import google.generativeai as genai
import lancedb
import pandas as pd
from pathlib import Path

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# -------------------------------------------------
# Embedding model setup
# -------------------------------------------------
embedding_model = "models/text-embedding-004"

def embed_text(text: str):
    """Generate embeddings for a given text."""
    result = genai.embed_content(
        model=embedding_model,
        content=text,
        task_type="retrieval_document"
    )
    return result["embedding"]

# -------------------------------------------------
# Open or create LanceDB database
# -------------------------------------------------
db_path = "lancedb"
db = lancedb.connect(db_path)
table_name = "transcripts"

# -------------------------------------------------
# Load transcript files
# -------------------------------------------------
transcripts_path = Path("data/transcripts")

def load_transcripts():
    """Load all transcript files from the transcripts directory."""
    documents = []

    for file_path in transcripts_path.glob("*.md"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "filename": file_path.name,
            "text": text
        })

    return documents

# -------------------------------------------------
# Step 5: Generate embeddings for all documents
# -------------------------------------------------
def prepare_documents_for_db():
    """Load transcripts and generate embeddings for each document."""
    docs = load_transcripts()
    prepared = []

    for doc in docs:
        embedding = embed_text(doc["text"])

        prepared.append({
            "filename": doc["filename"],
            "text": doc["text"],
            "embedding": embedding
        })

    return prepared

# -------------------------------------------------
# Step 6: Save documents + embeddings into LanceDB
# -------------------------------------------------
def save_to_lancedb():
    """Create or overwrite LanceDB table with embedded documents."""
    prepared_docs = prepare_documents_for_db()

def save_to_lancedb():
    """Create or overwrite LanceDB table with embedded documents."""
    prepared_docs = prepare_documents_for_db()

    df = pd.DataFrame(prepared_docs)

    # If table exists → clear it
    if table_name in db.table_names():
        print("Table exists — overwriting…")
        table = db.open_table(table_name)
        table.delete(where="filename IS NOT NULL")
    else:
        print("Creating new table…")
        table = db.create_table(
            table_name,
            df.to_dict(orient="records")
        )

    # Insert all documents
    table.add(df.to_dict(orient="records"))
    print("Saved", len(df), "documents to LanceDB.")

    return table



# -------------------------------------------------
# Test block (runs only when you execute the file)
# -------------------------------------------------
if __name__ == "__main__":
    # Test embedding
    test_text = "Detta är ett test."
    embedding = embed_text(test_text)
    print("Embedding längd:", len(embedding))
    print("Första 5 värden:", embedding[:5])

    # Test Step 4
    docs = load_transcripts()
    print("Antal filer hittade:", len(docs))

    # Test Step 5
    prepared_docs = prepare_documents_for_db()
    print("Antal embeddings skapade:", len(prepared_docs))

    # Test Step 6
    table = save_to_lancedb()
    print("Tabell klar i LanceDB:", table)
