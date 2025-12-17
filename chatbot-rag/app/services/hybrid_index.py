from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from app.db.sqlite_store import load_all_chunks
from app.config import VECTORSTORE_PATH


def rebuild_faiss_from_sqlite():
    texts, vectors, sources = load_all_chunks()

    docs = [
        Document(page_content=text, metadata={"source": src})
        for text, src in zip(texts, sources)
    ]

    embeddings = OpenAIEmbeddings()

    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTORSTORE_PATH)

    print(" FAISS sincronizado desde SQLite")
