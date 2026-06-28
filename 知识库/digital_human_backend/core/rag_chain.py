"""RAG 问答链 - 基于检索增强生成。"""

from typing import Optional

from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from config.settings import get_llm
from core.vector_store import load_vector_store, get_retriever


RAG_PROMPT_TEMPLATE = """你是一个专业的知识库助手。请严格根据以下上下文信息回答问题。
如果上下文中没有相关信息，请明确告知用户你无法基于现有知识库回答该问题，不要编造答案。
请用中文回答。

上下文信息：
{context}

用户问题：{question}

回答："""

RAG_PROMPT = PromptTemplate(
    template=RAG_PROMPT_TEMPLATE,
    input_variables=["context", "question"],
)


def create_rag_chain(persist_path: Optional[str] = None):
    """创建 RAG 问答链。"""
    vector_store = load_vector_store(persist_path)
    retriever = get_retriever(vector_store, k=3)
    llm = get_llm()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": RAG_PROMPT},
    )
    return qa_chain


def query_rag(question: str, persist_path: Optional[str] = None) -> dict:
    """直接调用 RAG 问答，返回结果字典。"""
    chain = create_rag_chain(persist_path)
    result = chain.invoke({"query": question})
    return {
        "answer": result.get("result", ""),
        "sources": [
            {
                "content": doc.page_content[:200],
                "metadata": doc.metadata,
            }
            for doc in result.get("source_documents", [])
        ],
    }
