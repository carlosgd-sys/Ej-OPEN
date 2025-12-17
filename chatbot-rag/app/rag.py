from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

from app.db.vectorstore import load_vectorstore
from app.config import OPENAI_MODEL

# Vector store
db = load_vectorstore()
retriever = db.as_retriever(search_kwargs={"k": 4})

# LLM
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0
)

#  MEMORIA SIMPLE (en RAM)
chat_history = []

# Prompt conversacional
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un asistente conversacional. "
     "Responde usando SOLO el contexto de los documentos y la conversación previa. "
     "Si algo no está en los documentos, dilo."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
    ("system", "Contexto:\n{context}")
])


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


chain = (
    {
        "context": retriever | format_docs,
        "question": lambda x: x,
        "history": lambda _: chat_history,
    }
    | prompt
    | llm
    | StrOutputParser()
)


def ask_question(question: str) -> str:
    # Ejecutar cadena
    answer = chain.invoke(question)

    # Guardar conversación
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=answer))

    return answer
