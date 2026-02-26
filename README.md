# React + Vite
# RAG Assistant – Retrieval Augmented Generation System

## Project Overview
This project implements a Retrieval Augmented Generation (RAG) based assistant that answers user questions using a predefined knowledge base.  
Instead of relying on an external paid LLM, the system retrieves the most relevant document chunks using embeddings and cosine similarity, then generates grounded responses strictly from the retrieved content.

The project satisfies all assignment requirements including backend API, retrieval logic, frontend chat interface, session handling, and robust error handling.

---

## Architecture Diagram

## Architecture Diagram

## Architecture Diagram

```mermaid
flowchart LR
    U["User<br/>(Web Browser)"]
    F["Frontend<br/>React + Vite"]
    B["Backend API<br/>FastAPI"]
    E["Embedding Model<br/>all-MiniLM-L6-v2"]
    V["Vector Store<br/>vector_store.json"]
    R["Grounded Response Builder"]

    U -->|Ask Question| F
    F -->|POST /api/chat<br/>sessionId| B
    B -->|Encode Query| E
    E -->|Embedding Vector| B
    B -->|Cosine Similarity| V
    V -->|Top-K Chunks| B
    B -->|Docs > Chat History| R
    R -->|Final Answer| F
    F -->|Display Response| U

## RAG Workflow Explanation

1. The user enters a question in the frontend chat interface.
2. The frontend sends the question and sessionId to the backend API.
3. The backend converts the user question into an embedding vector.
4. The query embedding is compared with stored document embeddings using cosine similarity.
5. The top 3 most relevant document chunks are retrieved.
6. The assistant response is generated strictly from retrieved document content.
7. The response is returned to the frontend and displayed to the user.

This workflow ensures accurate, grounded, and non-hallucinated responses.

---

## Embedding Strategy

- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Reason for Selection:**
  - Lightweight and fast
  - High-quality semantic embeddings
  - Fully local and cost-free

### Process
- Each document chunk is converted into an embedding vector.
- User queries are embedded using the same model.
- All embeddings exist in the same vector space, allowing direct comparison.

---

## Similarity Search Explanation

- **Similarity Metric:** Cosine Similarity
- **Top-K Retrieval:** 3 chunks
- **Similarity Threshold:** 0.6

Cosine similarity measures the semantic closeness between vectors and is widely used in information retrieval systems.

Only chunks exceeding the threshold are considered relevant.

---

## Prompt Design Reasoning

- The system uses only retrieved document content to construct answers.
- No external knowledge or hallucinated content is added.
- If no relevant documents are found, the assistant clearly states that it lacks sufficient information.
- A controlled temperature value (0.2) ensures deterministic and stable responses.

---

## Context Handling

- The system maintains the last 3–5 message pairs per session.
- Sessions are tracked using a sessionId stored in browser localStorage.
- Chat history improves conversational continuity.
- Document grounding always has priority over chat history.

---

## Frontend Features

- Input field
- Send button
- User and assistant message display
- Loading indicator
- Session handling using localStorage
- New Chat button
- Auto-scroll to latest message
- Message timestamps

Built using React and Vite.

---

## Backend Features

- FastAPI REST API
- Local embedding model
- Vector similarity retrieval
- Timeout handling
- API failure handling
- Clean and modular architecture

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 20+
- npm
- Git

---

### Backend Setup

```bash
cd rag-assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.server:app --reload
cd frontend
npm run dev
