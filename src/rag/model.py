import asyncio
from pydantic import BaseModel
from pydantic_ai import Agent
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Import retriever
from ..retrieval.retriever import retrieve_relevant_docs

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

genai.configure(api_key=GOOGLE_API_KEY)

# -------------------------------------------------
# Output schema
# -------------------------------------------------
class Answer(BaseModel):
    answer: str
    sources: list[str]

# -------------------------------------------------
# System prompt
# -------------------------------------------------
SYSTEM_PROMPT = """
Du är en hjälpsam AI-assistent som svarar baserat på Said Abdis kursmaterial.
Använd alltid dokumenten som hämtas av retrieval.
Skriv tydligt, korrekt och ange källor i svaret.
"""

# -------------------------------------------------
# Build agent
# -------------------------------------------------
agent = Agent(
    model="gemini-2.5-flash",
    system_prompt=SYSTEM_PROMPT
)

# -------------------------------------------------
# ASYNC RAG pipeline
# -------------------------------------------------
async def run_rag(query: str) -> Answer:
    """Retrieve documents + run RAG model."""

    # 1. Retrieve docs
    retrieved_docs = retrieve_relevant_docs(query, k=3)

    context = "\n\n".join(
        f"--- från {d['filename']} ---\n{d['text']}"
        for d in retrieved_docs
    )

    full_query = f"""
Fråga: {query}

Relevant kursmaterial:
{context}

Svara utförligt och ange vilka filer du använde.
"""

    # 2. Await agent.run()
    result = await agent.run(full_query)

    # -------------------------------------------------
    # UNIVERSAL RESULT EXTRACTION
    # -------------------------------------------------

    if hasattr(result, "output_text"):
        output_text = result.output_text
    elif hasattr(result, "text"):
        output_text = result.text
    elif hasattr(result, "output"):
        output_text = result.output
    else:
        raise ValueError("Kunde inte läsa ut text från AgentRunResult.")

    # 3. Build Answer model
    sources = [d["filename"] for d in retrieved_docs]

    return Answer(answer=output_text, sources=sources)

# -------------------------------------------------
# Test
# -------------------------------------------------
if __name__ == "__main__":
    print("🔍 Testing RAG model...\n")

    query = "Vad är logistic regression?"
    response = asyncio.run(run_rag(query))

    print("Svar:\n")
    print(response.answer)

    print("\nKällor:")
    print(response.sources)
