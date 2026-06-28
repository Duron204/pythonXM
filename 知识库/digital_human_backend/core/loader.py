"""多格式文档加载器 - 支持 PDF / TXT / Markdown。"""

from typing import List
from pathlib import Path
from langchain_core.documents import Document


def load_document(file_path: str) -> List[Document]:
    """根据文件扩展名加载文档，返回 LangChain Document 列表。"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return _load_pdf(path)
    elif suffix in (".txt", ".md", ".markdown"):
        return _load_text(path)
    else:
        raise ValueError(f"不支持的文件格式: {suffix}")


def _load_pdf(path: Path) -> List[Document]:
    from langchain_community.document_loaders import PyPDFLoader

    loader = PyPDFLoader(str(path))
    return loader.load()


def _load_text(path: Path) -> List[Document]:
    from langchain_community.document_loaders import TextLoader

    loader = TextLoader(str(path), encoding="utf-8")
    return loader.load()
