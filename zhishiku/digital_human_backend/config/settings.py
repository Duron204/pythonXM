"""配置管理模块 - 加载 .env 并提供全局配置。"""

import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# ---------- 基础配置 ----------
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "llama3:8b")
EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store/chroma_db")
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")
TTS_LANG = os.getenv("TTS_LANG", "zh")


def get_embedding_model() -> HuggingFaceEmbeddings:
    """返回本地 HuggingFace Embedding 模型实例。"""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_llm(temperature: float = 0.7) -> ChatOllama:
    """返回本地 Ollama LLM 实例。"""
    return ChatOllama(
        model=LOCAL_LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
    )
