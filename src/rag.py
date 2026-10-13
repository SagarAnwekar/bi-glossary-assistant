"""BI Glossary Assistant: small RAG over own-written KPI definitions.
Needs GEMINI_API_KEY in the environment."""
import os, pathlib
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.documents import Document

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemini-3.1-flash-lite")
EMBED_MODEL = "models/gemini-embedding-001"
PROMPT = ("You answer questions about business KPI definitions using ONLY the context below.\n"
          "If the context does not contain the answer, reply exactly: I don't know based on the glossary.\n\n"
          "Context:\n{context}\n\nQuestion: {question}\nAnswer in 1-3 sentences.")

def load_docs():
    return [Document(page_content=p.read_text(), metadata={"source": p.stem}) for p in sorted(DOCS.glob("*.md"))]

def build_index(chunk_size=400, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(load_docs())
    emb = GoogleGenerativeAIEmbeddings(model=EMBED_MODEL)
    return FAISS.from_documents(chunks, emb), len(chunks)

def answer(store, question, k=3):
    hits = store.similarity_search(question, k=k)
    return ask_llm(question, hits), [h.metadata["source"] for h in hits]

def ask_llm(question, hits):
    ctx = "\n---\n".join(h.page_content for h in hits)
    llm = ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0)
    return llm.invoke(PROMPT.format(context=ctx, question=question)).text.strip()
