"""文本分割器 - 将长文档切分为适合向量化的块。"""

from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    docs: List[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> List[Document]:
    """将文档列表分割为更小的块，过滤空块。"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    # 过滤空块
    return [c for c in chunks if c.page_content and c.page_content.strip()]
