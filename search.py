"""
Search Module
Handles cosine similarity calculation and ranking search results.
"""

from typing import List, Dict, Any
import numpy as np


def compute_cosine_similarity(query_vector: np.ndarray, chunk_vectors: np.ndarray) -> np.ndarray:
    """
    Computes cosine similarity between a single query vector and multiple chunk vectors.

    Cosine Similarity Formula:
        sim(A, B) = (A · B) / (||A|| * ||B||)

    Args:
        query_vector: 1D numpy array representing query embedding.
        chunk_vectors: 2D numpy array of shape (N, dim) representing chunk embeddings.

    Returns:
        1D numpy array of similarity scores between -1.0 and 1.0 (typically 0.0 to 1.0 for embeddings).
    """
    if chunk_vectors.size == 0 or query_vector.size == 0:
        return np.array([])

    # Compute dot product between query vector and each chunk vector
    dot_products = np.dot(chunk_vectors, query_vector)

    # Compute L2 norms (magnitudes)
    query_norm = np.linalg.norm(query_vector)
    chunk_norms = np.linalg.norm(chunk_vectors, axis=1)

    # Avoid division by zero by replacing 0 norms with a small epsilon
    epsilon = 1e-10
    denominator = (chunk_norms * query_norm)
    denominator[denominator == 0] = epsilon

    # Cosine similarity scores
    similarity_scores = dot_products / denominator
    return similarity_scores


def rank_search_results(
    chunks: List[Dict[str, Any]],
    similarity_scores: np.ndarray,
    top_k: int = 5,
    threshold: float = 0.0
) -> List[Dict[str, Any]]:
    """
    Ranks text chunks based on their similarity scores and returns the top K matches.

    Args:
        chunks: List of chunk dictionaries containing 'text', 'page', etc.
        similarity_scores: 1D numpy array of similarity scores corresponding to chunks.
        top_k: Maximum number of top results to return.
        threshold: Minimum similarity score threshold (0.0 to 1.0).

    Returns:
        List of result dictionaries sorted by similarity score descending.
    """
    if len(chunks) == 0 or similarity_scores.size == 0:
        return []

    results = []
    for idx, score in enumerate(similarity_scores):
        if score >= threshold:
            results.append({
                "chunk_id": chunks[idx].get("chunk_id", idx),
                "page": chunks[idx].get("page", 1),
                "text": chunks[idx]["text"],
                "score": float(score),
                "similarity_percentage": round(float(score) * 100, 1)
            })

    # Sort results by similarity score in descending order
    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]
