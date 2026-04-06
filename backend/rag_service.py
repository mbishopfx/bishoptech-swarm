import os
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document as LCDocument
from sqlalchemy import create_engine, text
from database import DATABASE_URL

# Embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Connection string for PGVector
CONNECTION_STRING = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")

def init_vector_db():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

def get_vector_store(collection_name: str):
    return PGVector(
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
        collection_name=collection_name,
    )

def add_documents_to_rag(kb_id: int, filename: str, content: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(content)
    
    docs = [
        LCDocument(page_content=chunk, metadata={"kb_id": kb_id, "filename": filename})
        for chunk in chunks
    ]
    
    vector_store = get_vector_store(f"kb_{kb_id}")
    vector_store.add_documents(docs)

def query_rag(kb_id: int, query: str, k: int = 3):
    vector_store = get_vector_store(f"kb_{kb_id}")
    results = vector_store.similarity_search(query, k=k)
    
    context = "\n\n".join([doc.page_content for doc in results])
    return context
