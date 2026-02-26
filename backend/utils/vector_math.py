import numpy as np

def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two vectors
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0

    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
def retrieve_top_chunks(
    query_embedding,
    vector_store,
    top_k=3,
    threshold=0.6
):
    """
    Retrieve top-k most similar chunks based on cosine similarity
    """
    scored_chunks = []
    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        if score >= threshold:
            scored_chunks.append({
                "chunk_id": item["chunk_id"],
                "title": item["title"],
                "content": item["content"],
                "score": score
            })
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    return scored_chunks[:top_k]