"""向量数据库管理 - 构建、加载、检索。"""

from typing import List, Optional
from langchain_core.documents import Document
from langchain_chroma import Chroma

from config.settings import get_embedding_model, VECTOR_STORE_PATH


def create_vector_store(
    docs: List[Document],
    persist_path: Optional[str] = None,
) -> Chroma:
    """从文档列表构建 Chroma 向量库并持久化。"""
    persist_path = persist_path or VECTOR_STORE_PATH
    embedding = get_embedding_model()
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=persist_path,
    )
    print(f"[向量库] 构建完成，共 {len(docs)} 个文本块 -> {persist_path}")
    return vector_store


def load_vector_store(persist_path: Optional[str] = None) -> Chroma:
    """加载已有的向量库。"""
    persist_path = persist_path or VECTOR_STORE_PATH
    embedding = get_embedding_model()
    vector_store = Chroma(
        persist_directory=persist_path,
        embedding_function=embedding,
    )
    results = vector_store.get()
    count = len(results.get("ids", []))
    print(f"[向量库] 加载完成，共 {count} 条记录 <- {persist_path}")
    return vector_store


def get_retriever(vector_store: Chroma, k: int = 3):
    """返回检索器。"""
    return vector_store.as_retriever(search_kwargs={"k": k})
