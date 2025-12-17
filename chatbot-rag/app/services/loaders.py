from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
)


def load_file(path: str):
    if path.endswith(".pdf"):
        return PyPDFLoader(path).load()

    elif path.endswith(".txt"):
        # 🔧 Solución encoding Windows
        return TextLoader(
            path,
            encoding="utf-8",
            autodetect_encoding=True
        ).load()

    elif path.endswith(".csv"):
        return CSVLoader(path).load()

    else:
        return []
