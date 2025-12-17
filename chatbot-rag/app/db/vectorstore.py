import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from app.services.loaders import load_file
from app.db.sqlite_store import save_chunks, init_db
from app.services.hybrid_index import rebuild_faiss_from_sqlite
from app.config import CHUNK_SIZE, CHUNK_OVERLAP
from app.services.loaders import load_file
from app.config import (
    DOCS_PATH,
    VECTORSTORE_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL
)


def index_file_hybrid(file_path: str):
    init_db()

    documents = load_file(file_path)
    if not documents:
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    docs = splitter.split_documents(documents)
    texts = [d.page_content for d in docs]

    embeddings = OpenAIEmbeddings()
    vectors = embeddings.embed_documents(texts)

    doc_id = hashlib.md5(file_path.encode()).hexdigest()
    source = file_path.split("/")[-1]

    # 1️⃣ Guardar en SQLite
    save_chunks(doc_id, source, texts, vectors)

    # 2️⃣ Sincronizar FAISS
    rebuild_faiss_from_sqlite()


def build_vectorstore():
    documents = []

    for file in os.listdir(DOCS_PATH):
        documents.extend(load_file(f"{DOCS_PATH}/{file}"))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTORSTORE_PATH)


def load_vectorstore():
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
