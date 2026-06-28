# 数字人大脑后端服务

基于本地大模型的数字人"大脑"后端，支持 RAG 知识库问答、Agent 工具调用、WebSocket 语音交互。

## 技术栈

- **LLM**: Ollama 本地模型（qwen2:7b / llama3:8b）
- **RAG**: LangChain + Chroma 向量数据库
- **Embedding**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2（本地运行）
- **STT**: OpenAI Whisper（本地模型）
- **TTS**: gTTS（Google Text-to-Speech）
- **API**: FastAPI + WebSocket

## 快速开始

### 1. 安装 Ollama

访问 [ollama.ai](https://ollama.ai) 下载安装 Ollama，然后拉取模型：

```bash
# 推荐使用 qwen2:7b（中文能力较强）
ollama pull qwen2:7b

# 或者使用 llama3:8b
ollama pull llama3:8b
```

### 2. 准备 Python 环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate        # Linux/Mac
# 或 venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，根据需要修改：
# - LOCAL_LLM_MODEL：使用的模型名称
# - OLLAMA_BASE_URL：Ollama 服务地址
```

### 4. 构建知识库向量索引

```bash
# 将知识库文件（PDF/TXT/MD）放入 documents/ 目录
# 然后运行构建脚本
python scripts/build_vector_store.py
```

### 5. 启动服务

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

服务启动后访问：
- 文档页面: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 6. 测试

```bash
# 文本对话测试
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，请介绍一下你自己"}'

# WebSocket 测试
python scripts/test_voice.py
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 服务状态 |
| GET | `/health` | 健康检查 |
| POST | `/chat` | 文本对话 |
| POST | `/reset` | 重置会话 |
| WS | `/voice` | WebSocket 语音交互 |

## WebSocket 协议

连接 `ws://localhost:8000/voice` 后：

- 发送 **文本**: 直接对话
- 发送 **二进制**: 音频数据（WAV/MP3）
- 发送 `"RESET"`: 重置会话
- 发送 `"STOP"`: 断开连接

服务端返回：
- JSON: `{"type": "stt_result", "text": "..."}` - STT 结果
- JSON: `{"type": "text_reply", "text": "..."}` - AI 回复文本
- 二进制: TTS 音频数据（MP3 格式）

## 项目结构

```
digital_human_backend/
├── .env.example           # 环境变量模板
├── requirements.txt       # Python 依赖
├── config/
│   └── settings.py        # 配置管理
├── core/
│   ├── loader.py          # 文档加载器
│   ├── splitter.py        # 文本分割器
│   ├── vector_store.py    # 向量库管理
│   ├── rag_chain.py       # RAG 问答链
│   ├── tools.py           # Agent 工具
│   ├── agent.py           # Agent 核心逻辑
│   └── memory.py          # 对话记忆
├── voice/
│   ├── stt.py             # 语音转文字
│   ├── tts.py             # 文字转语音
│   └── audio_utils.py     # 音频工具
├── server.py              # FastAPI 主程序
├── scripts/
│   ├── build_vector_store.py  # 构建向量库
│   └── test_voice.py          # 测试脚本
├── documents/             # 知识库源文件
└── vector_store/          # 向量库持久化
```

## 常见问题

### Ollama 连接失败
- 确保 Ollama 已启动：`ollama serve`
- 检查端口是否正确（默认 11434）
- 确认模型已拉取：`ollama list`

### 模型下载慢
- 使用国内镜像或代理
- 选择较小的模型如 `qwen2:7b` 替代 `llama3:8b`

### Whisper 加载慢
- 首次加载需要下载模型，之后会缓存到本地
- 可在 `.env` 中将 `WHISPER_MODEL_SIZE` 改为 `tiny` 加速

### 内存不足
- 使用较小的 LLM 模型（如 `qwen2:3b`）
- 将 Whisper 模型改为 `tiny`

## License

MIT
