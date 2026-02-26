import json
import os
import time
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from backend.utils.vector_math import retrieve_top_chunks

TEMPERATURE = 0.2
TIMEOUT_SECONDS = 5
MAX_HISTORY_PAIRS = 5   
SIMILARITY_THRESHOLD = 0.6
TOP_K = 3

model = SentenceTransformer("all-MiniLM-L6-v2")


VECTOR_STORE_PATH = os.path.join("backend", "data", "vector_store.json")
with open(VECTOR_STORE_PATH, "r", encoding="utf-8") as f:
    VECTOR_STORE = json.load(f)


SESSION_STORE: Dict[str, List[dict]] = {}


app = FastAPI(title="RAG Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    sessionId: str

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    start_time = time.time()

    try:
        user_question = request.message.strip()
        session_id = request.sessionId

        if not user_question:
            raise HTTPException(status_code=400, detail="Empty message")


        if time.time() - start_time > TIMEOUT_SECONDS:
            raise HTTPException(status_code=504, detail="Request timeout")


        if session_id not in SESSION_STORE:
            SESSION_STORE[session_id] = []


        history = SESSION_STORE[session_id]

        previous_user_messages = [
            msg["content"]
            for msg in history
            if msg["role"] == "user"
        ]

        contextual_query = " ".join(
            previous_user_messages[-MAX_HISTORY_PAIRS:]
        )

        full_query = f"{contextual_query} {user_question}".strip()

        query_embedding = model.encode(full_query).tolist()


        top_chunks = retrieve_top_chunks(
            query_embedding=query_embedding,
            vector_store=VECTOR_STORE,
            top_k=TOP_K,
            threshold=SIMILARITY_THRESHOLD
        )

        if not top_chunks:
            assistant_reply = (
                "I do not have enough information to answer that "
                "based on the available documents."
            )
        else:
            assistant_reply = top_chunks[0]["content"]

        SESSION_STORE[session_id].append({
            "role": "user",
            "content": user_question
        })

        SESSION_STORE[session_id].append({
            "role": "assistant",
            "content": assistant_reply
        })

   
        SESSION_STORE[session_id] = SESSION_STORE[session_id][-MAX_HISTORY_PAIRS * 2 :]

  
        return {
            "answer": assistant_reply,
            "temperature": TEMPERATURE,
            "sessionId": session_id,
            "historySize": len(SESSION_STORE[session_id])
        }

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="System error. Please try again later."
        )