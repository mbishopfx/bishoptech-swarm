import os
from sqlalchemy import create_engine, text
from database import DATABASE_URL

RAG_ENABLED = DATABASE_URL.startswith("postgresql")


def init_vector_db():
    if not RAG_ENABLED:
        return

    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
    except Exception as exc:
        print(f"Warning: RAG init skipped: {exc}")


def add_documents_to_rag(kb_id: int, filename: str, content: str):
    if not RAG_ENABLED:
        return

    # RAG is optional on Railway; keep the call safe even if the vector stack is absent.
    try:
        from langchain_community.vectorstores import PGVector
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.docstore.document import Document as LCDocument
    except Exception as exc:
        print(f"Warning: RAG document ingestion skipped: {exc}")
        return

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    connection_string = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(content)

    docs = [
        LCDocument(page_content=chunk, metadata={"kb_id": kb_id, "filename": filename})
        for chunk in chunks
    ]

    vector_store = PGVector(
        connection_string=connection_string,
        embedding_function=embeddings,
        collection_name=f"kb_{kb_id}",
    )
    vector_store.add_documents(docs)


def query_rag(kb_id: int, query: str, k: int = 3):
    if not RAG_ENABLED:
        return ""

    try:
        from langchain_community.vectorstores import PGVector
        from langchain_community.embeddings import HuggingFaceEmbeddings
    except Exception as exc:
        print(f"Warning: RAG query skipped: {exc}")
        return ""

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    connection_string = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    vector_store = PGVector(
        connection_string=connection_string,
        embedding_function=embeddings,
        collection_name=f"kb_{kb_id}",
    )
    results = vector_store.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])
