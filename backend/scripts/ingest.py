import json
import os
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
DOCS_PATH = os.path.join("backend", "data", "docs.json")
OUTPUT_PATH = os.path.join("backend", "data", "vector_store.json")
CHUNK_SIZE = 300
OVERLAP = 50
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
    return chunks
def generate_embedding(text):
    embedding = model.encode(text)
    return embedding.tolist()
def main():
    with open(DOCS_PATH, "r", encoding="utf-8") as f:
        documents = json.load(f)
    vector_store = []
    for doc in documents:
        doc_id = doc["id"]
        title = doc["title"]
        content = doc["content"]

        chunks = chunk_text(content, CHUNK_SIZE, OVERLAP)

        for idx, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)

            vector_store.append({
                "chunk_id": f"{doc_id}_chunk_{idx + 1}",
                "title": title,
                "content": chunk,
                "embedding": embedding
            })

            print(f"Embedded {doc_id}_chunk_{idx + 1}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(vector_store, f, indent=2)
    print("embeddings generated using local model.")
if __name__ == "__main__":
    main()