"""独立脚本：扫描 documents/ 目录并构建/更新向量库。"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.loader import load_document
from core.splitter import split_documents
from core.vector_store import create_vector_store
from config.settings import VECTOR_STORE_PATH

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown"}


def main():
    docs_dir = Path(__file__).resolve().parent.parent / "documents"
    if not docs_dir.exists():
        print(f"[错误] 文档目录不存在: {docs_dir}")
        print("请创建 documents/ 目录并放入知识库文件。")
        return

    all_files = []
    for f in docs_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
            all_files.append(f)

    if not all_files:
        print(f"[提示] documents/ 目录下未找到支持的文件（{', '.join(SUPPORTED_EXTENSIONS)}）")
        print("请放入文件后重新运行此脚本。")
        return

    print(f"[信息] 找到 {len(all_files)} 个文件待处理")

    all_docs = []
    for f in all_files:
        try:
            docs = load_document(str(f))
            all_docs.extend(docs)
            print(f"  [OK] {f.name}: {len(docs)} 页/段")
        except Exception as e:
            print(f"  [FAIL] {f.name}: {e}")

    if not all_docs:
        print("[错误] 未能加载任何文档内容。")
        return

    print(f"\n[信息] 共加载 {len(all_docs)} 个文档片段，开始分割...")

    chunks = split_documents(all_docs)
    print(f"[信息] 分割完成，共 {len(chunks)} 个文本块")

    # 确保持久化目录存在
    persist_dir = Path(VECTOR_STORE_PATH)
    persist_dir.parent.mkdir(parents=True, exist_ok=True)

    create_vector_store(chunks, str(persist_dir))
    print(f"\n[完成] 向量库构建成功！路径: {persist_dir}")


if __name__ == "__main__":
    main()
