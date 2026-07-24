"""
Embeddings Module
Handles sentence transformer model loading and text embedding generation.
Uses 'all-MiniLM-L6-v2' to convert text into semantic vector representations.
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

# Global cache key or standard model identifier
MODEL_NAME = "all-MiniLM-L6-v2"


def load_model() -> SentenceTransformer:
    """
    Loads and returns the SentenceTransformer model.
    In Streamlit app, this function can be wrapped with @st.cache_resource.

    Returns:
        SentenceTransformer instance.
    """
    model = SentenceTransformer(MODEL_NAME)
    return model


def generate_chunk_embeddings(model: SentenceTransformer, text_chunks: List[str]) -> np.ndarray:
    """
    Generates embeddings for a list of text chunks.

    Args:
        model: Loaded SentenceTransformer model
        text_chunks: List of string chunks to embed

    Returns:
        Numpy array of shape (N, embedding_dim) containing vector embeddings.
    """
    if not text_chunks:
        return np.array([])

    embeddings = model.encode(text_chunks, show_progress_bar=False, convert_to_numpy=True)
    return embeddings


def generate_query_embedding(model: SentenceTransformer, query: str) -> np.ndarray:
    """
    Generates an embedding vector for a search query string.

    Args:
        model: Loaded SentenceTransformer model
        query: User search query string

    Returns:
        1D Numpy array representing the query embedding vector.
    """
    query_embedding = model.encode(query, show_progress_bar=False, convert_to_numpy=True)
    return query_embedding
