"""FastAPI 主程序 - WebSocket 语音交互端点。"""

import asyncio
import logging
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from config.settings import WHISPER_MODEL_SIZE, TTS_LANG
from core.agent import DigitalHumanAgent
from voice.stt import transcribe
from voice.tts import synthesize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="数字人大脑后端", version="1.0.0")

# 全局 Agent 实例
agent = DigitalHumanAgent()


@app.get("/")
async def root():
    return {"message": "数字人大脑后端服务运行中", "status": "ok"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat")
async def text_chat(payload: dict):
    """文本对话接口 - 用于测试或不带语音的场景。"""
    user_input = payload.get("message", "")
    if not user_input:
        return JSONResponse(status_code=400, content={"error": "message 不能为空"})
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, agent.chat, user_input)
        return {"reply": response}
    except Exception as e:
        logger.error(f"文本对话出错: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/reset")
async def reset_session():
    """重置当前会话记忆。"""
    agent.reset()
    return {"message": "会话已重置"}


@app.websocket("/voice")
async def voice_websocket(websocket: WebSocket):
    """WebSocket 语音交互端点。

    协议流程：
    1. 客户端连接
    2. 客户端发送音频二进制数据（支持 WAV/MP3/PCM）
    3. 服务端执行 STT -> Agent 处理 -> TTS
    4. 服务端返回音频二进制数据 + JSON 元信息

    客户端可通过发送文本消息 "RESET" 重置会话。
    客户端可通过发送文本消息 "STOP" 断开连接。
    """
    await websocket.accept()
    logger.info("[WS] 客户端已连接")

    try:
        while True:
            data = await websocket.receive()

            # 处理文本消息（控制指令）
            if "text" in data:
                text = data["text"]
                if text.strip().upper() == "RESET":
                    agent.reset()
                    await websocket.send_json({"type": "info", "message": "会话已重置"})
                    continue
                elif text.strip().upper() == "STOP":
                    await websocket.send_json({"type": "info", "message": "连接即将关闭"})
                    break
                # 文本消息也作为对话输入
                loop = asyncio.get_running_loop()
                reply_text = await loop.run_in_executor(None, agent.chat, text)
                reply_audio = await loop.run_in_executor(
                    None, synthesize, reply_text, TTS_LANG
                )
                # 先发送元信息 JSON，再发送音频
                import json
                meta = json.dumps({"type": "text_reply", "text": reply_text})
                await websocket.send_text(meta)
                if reply_audio:
                    await websocket.send_bytes(reply_audio)
                continue

            # 处理二进制音频数据
            if "bytes" in data:
                audio_data = data["bytes"]
                if not audio_data:
                    continue

                logger.info(f"[WS] 收到音频数据: {len(audio_data)} bytes")

                # 1. STT：语音转文字
                loop = asyncio.get_running_loop()
                user_text = await loop.run_in_executor(
                    None, transcribe, audio_data, WHISPER_MODEL_SIZE
                )

                if not user_text:
                    error_audio = await loop.run_in_executor(
                        None, synthesize, "抱歉，我没有听清，请再说一次。", TTS_LANG
                    )
                    if error_audio:
                        await websocket.send_json({"type": "text_reply", "text": "抱歉，我没有听清，请再说一次。"})
                        await websocket.send_bytes(error_audio)
                    continue

                logger.info(f"[WS] STT 结果: {user_text}")
                await websocket.send_json({"type": "stt_result", "text": user_text})

                # 2. Agent 处理
                reply_text = await loop.run_in_executor(None, agent.chat, user_text)
                logger.info(f"[WS] Agent 回复: {reply_text[:100]}...")
                await websocket.send_json({"type": "text_reply", "text": reply_text})

                # 3. TTS：文字转语音
                reply_audio = await loop.run_in_executor(
                    None, synthesize, reply_text, TTS_LANG
                )
                if reply_audio:
                    await websocket.send_bytes(reply_audio)
                    logger.info(f"[WS] 返回音频: {len(reply_audio)} bytes")
                else:
                    logger.warning("[WS] TTS 返回空音频")

    except WebSocketDisconnect:
        logger.info("[WS] 客户端已断开连接")
    except Exception as e:
        logger.error(f"[WS] 异常: {e}")
        try:
            await websocket.close()
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
