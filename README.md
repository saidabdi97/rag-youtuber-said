# rag-youtuber-said
RAG chatbot trained on YouTube video transcripts.
Detta projekt är ett **Retrieval-Augmented Generation (RAG)-system** som kan svara på frågor baserat på kursmaterial i Markdown-format.  
Systemet kombinerar **vektorsökning** med en **språkmodell** för att generera faktabaserade, pedagogiska svar.

Projektet är uppbyggt så att:
- **Backend (API)** körs i **Azure Functions**
- **Frontend (UI)** körs **lokalt i Streamlit**
- Kursmaterial används som **enda kunskapskälla**

---

## 🎯 Syfte

Syftet med projektet är att:
- Visa förståelse för **RAG-arkitektur**
- Undvika hallucinationer genom att använda **retrieval från dokument**
- Bygga ett system som uppfyller kravet:
  > *Deploy your API to Azure Functions and connect it to a locally running Streamlit app*

---

## 🧠 Vad är RAG?

Retrieval-Augmented Generation innebär att:
1. Dokument delas upp och embedas
2. En användarfråga embedas
3. Relevanta dokument hämtas via vektorsökning
4. Språkmodellen genererar svar baserat på dokument + fråga

Detta gör svaren mer tillförlitliga än en vanlig LLM.

---

## 🏗️ Systemarkitektur



---

## 📁 Projektstruktur

rag-youtuber-said/
├── data/
│ └── transcripts/ # Kursmaterial i Markdown
├── lancedb/ # Vektordatabas (genererad lokalt)
├── src/
│ ├── ingestion/ # Läser & embedar dokument
│ ├── retrieval/ # Vektorsökning
│ ├── rag/ # Prompt + persona
│ │ └── persona/
│ │ └── default.txt
│ ├── api/ # FastAPI /rag-endpoint
│ └── frontend/ # Streamlit UI
├── function_app.py # Azure Functions entrypoint (ASGI)
├── host.json # Azure routing-konfiguration
├── requirements.txt
└── README.md


---

## 🤖 Persona

Systemet använder en **persona** som definierar ton och stil (kursassistent / pedagogisk YouTuber).  
Personan ligger i en separat textfil:


Detta gör det enkelt att ändra modellens beteende utan att ändra kod.

---

## ⚙️ Backend – FastAPI & Azure Functions

- Backend är byggd med **FastAPI**
- Exponerar endpointen:


- Deployad till **Azure Functions (Python runtime)**
- Använder **Function Key** för autentisering
- Miljövariabler hanteras via Azure App Settings

Azure Functions wrappar FastAPI med en ASGI-adapter:

```python
app = func.AsgiFunctionApp(
  app=fastapi_app,
  http_auth_level=func.AuthLevel.FUNCTION
)


"http": {
  "routePrefix": ""
}
GOOGLE_API_KEY=...
FUNCTION_APP_API=...

python src/ingestion/ingest.py

func start

streamlit run src/frontend/app.py

