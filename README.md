# Chatbot RAG con FastAPI, LangChain y Streaming

Este proyecto implementa un **chatbot RAG (Retrieval-Augmented Generation)** con FastAPI, LangChain y OpenAI, incluyendo:

- Chat conversacional
- Recuperación de datos de documentos (PDF, TXT, CSV)
- Vector store FAISS
- Streaming token a token (SSE)
- Captura de prospectos en SQLite
- Envío de correos SMTP bajo consentimiento
- Watcher automático para reindexado
- Gestión de dependencias con Poetry

---

## 1. Requisitos del sistema

- Python **3.12.x** (obligatorio)
- Git
- Acceso a una clave de OpenAI
- Cuenta SMTP (Gmail con App Password u otro proveedor)

---

## 2. Estructura del proyecto

```
chatbot-rag/
├── app/
│   ├── main.py
│   ├── rag.py
│   ├── rag_stream.py
│   ├── vectorstore.py
│   ├── prospects_db.py
│   ├── schemas.py
│   ├── config.py
│   ├── services/
│   │   ├── mailer.py
│   │   ├── intent.py
│   │   └── watcher.py
│   └── static/
│       └── index.html
├── data/
│   ├── docs/
│   ├── faiss_index/
│   └── prospects.db
    └── vectors.db
├── pyproject.toml
├── poetry.lock
├── .env
└── README.md
```

---

## 3. Instalación de Poetry

En Windows (PowerShell):

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Cerrar y volver a abrir la terminal.

Verificar instalación:

```
poetry --version
```

---

## 4. Configuración del entorno virtual

Todos los comandos se muestran de forma **agnóstica al PATH**, usando siempre `python -m` o `poetry run`, para evitar problemas en Windows.

Desde la raíz del proyecto:

```
poetry env use python3.12
poetry install
```

Esto crea el entorno virtual e instala las dependencias exactas.

---

## 5. Variables de entorno

Crear un archivo `.env` en la raíz:

```}
########################################
#  OPENAI CONFIGURATION
########################################

# API key de OpenAI (OBLIGATORIA)
# Se obtiene en https://platform.openai.com/
OPENAI_API_KEY=

# Modelo de lenguaje a usar para generación de respuestas
# Ejemplo: gpt-4o-mini, gpt-4.1-mini
OPENAI_MODEL=gpt-4o-mini

# Modelo de embeddings usado para indexar documentos
# Recomendado: text-embedding-3-small (rápido y barato)
EMBEDDING_MODEL=text-embedding-3-small


########################################
# RAG / VECTORSTORE CONFIGURATION
########################################

# Tamaño de cada chunk de texto al dividir documentos
# Valores comunes: 300–1000
CHUNK_SIZE=500

# Solapamiento entre chunks para mantener contexto
# Valores comunes: 20–100
CHUNK_OVERLAP=50

# Ruta donde se encuentran los documentos a indexar
# Puede ser relativa al root del proyecto
DOCS_PATH=data/docs

# Ruta donde se guarda / carga el índice FAISS
VECTORSTORE_PATH=data/faiss_index


########################################
#  SMTP / EMAIL CONFIGURATION
########################################
Nota: Para Gmail es obligatorio usar **App Password** con 2FA activado.

# Servidor SMTP para envío de correos
SMTP_HOST=smtp.gmail.com

# Puerto SMTP (587 para TLS, 465 para SSL)
SMTP_PORT=587

# Usuario SMTP (normalmente el correo)
SMTP_USER=

# Password o App Password del correo
SMTP_PASSWORD=

# Dirección "From" usada en los correos enviados
SMTP_FROM=



---

## 6. Carga de documentos

Colocar archivos en:

```
data/docs/
```

Formatos soportados:

- PDF
- TXT
- CSV

El watcher detecta cambios y reindexa automáticamente.

---

## 7. Inicialización manual del índice (opcional)

Usando ejecución agnóstica al PATH:

```
poetry run python -c "from app.db.vectorstore import build_vectorstore; build_vectorstore()"
```
poetry run python -c "from app.vectorstore import build_vectorstore; build_vectorstore()"
```

---

## 8. Ejecución del servidor

Modo desarrollo (agnóstico al PATH):

```
poetry run python -m uvicorn app.main:app --reload
```
poetry run uvicorn app.main:app --reload
```

Abrir en el navegador:

```
http://127.0.0.1:8000/
```

---

## 9. Endpoints disponibles

Todos los endpoints asumen que el servidor se ejecuta con `poetry run` o dentro de `poetry shell`.

### POST /chat

Entrada:

```
{
  "question": "Tu pregunta"
}
```

Salida:

```
{
  "answer": "respuesta",
  "show_form": false
}
```

### GET /chat/stream

```
/chat/stream?q=texto
```

Devuelve tokens vía Server-Sent Events.

### POST /prospect

```
{
  "name": "Nombre",
  "email": "correo",
  "message": "mensaje"
}
```

Guarda el prospecto y envía correo de confirmación.

---

## 10. Base de datos de prospectos

SQLite se crea automáticamente en:

```
data/prospects.db
```

Tabla:

- id
- name
- email
- message
- created_at

---

## 11. Streaming token a token

El streaming se implementa con:

- Server-Sent Events (SSE)
- OpenAI streaming

Permite UX fluida tipo ChatGPT.

---

## 12. Dependencias principales

- fastapi
- uvicorn
- langchain-core
- langchain-community
- langchain-openai
- faiss-cpu
- numpy < 2.0
- pydantic
- watchdog

---

## 13. Reglas importantes

- No usar NumPy 2.x
- No usar pip fuera de Poetry
- Usar Python 3.12 exclusivamente

Ajustar según necesidades del proyecto.


