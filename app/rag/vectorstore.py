from functools import lru_cache

from langchain_community.vectorstores import SupabaseVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from supabase import Client, create_client

from app.core.config import get_settings

settings = get_settings()

TABLE_NAME = "documents"
QUERY_NAME = "match_documents"

EMBEDDING_DIMENSIONS = {
    "sentence-transformers/all-minilm-l6-v2": 384,
    "all-minilm-l6-v2": 384,
    "baai/bge-small-en-v1.5": 384,
    "baai/bge-base-en-v1.5": 768,
    "sentence-transformers/all-mpnet-base-v2": 768,
}


def get_embedding_dimension(model_name: str | None = None) -> int:
    name = (model_name or settings.embedding_model or "").strip()
    if not name:
        raise RuntimeError("Embedding model is not configured")

    normalized = name.lower()
    if normalized in EMBEDDING_DIMENSIONS:
        return EMBEDDING_DIMENSIONS[normalized]
    if "all-minilm" in normalized:
        return 384

    raise ValueError(
        f"Unsupported embedding model '{name}'. "
        "Add the matching dimension to EMBEDDING_DIMENSIONS."
    )


@lru_cache
def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        encode_kwargs={"normalize_embeddings": True},
    )


@lru_cache
def get_supabase_client() -> Client:
    if not settings.supabase_url:
        raise RuntimeError("SUPABASE_URL is missing")
    if not settings.supabase_service_key:
        raise RuntimeError("SUPABASE_SERVICE_KEY is missing")
    return create_client(settings.supabase_url, settings.supabase_service_key)


@lru_cache
def get_vectorstore() -> SupabaseVectorStore:
    return SupabaseVectorStore(
        client=get_supabase_client(),
        embedding=get_embeddings(),
        table_name=TABLE_NAME,
        query_name=QUERY_NAME,
    )


def get_retriever():
    return get_vectorstore().as_retriever(
        search_kwargs={
            "k": settings.top_k,
            "filter": {"namespace": settings.kb_namespace},
        }
    )


def add_documents(chunks):
    for chunk in chunks:
        chunk.metadata["namespace"] = settings.kb_namespace
    return get_vectorstore().add_documents(chunks)