"""WebSocket 语音测试客户端脚本。

使用方法：
  1. 先启动服务端: uvicorn server:app --reload
  2. 运行此脚本: python scripts/test_voice.py
  3. 脚本会读取测试音频文件或从麦克风录音并发送到服务器
"""

import asyncio
import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import websockets
except ImportError:
    print("请先安装 websockets: pip install websockets")
    sys.exit(1)

SERVER_URL = "ws://localhost:8000/voice"
TEST_AUDIO_DIR = Path(__file__).resolve().parent.parent / "test_audio"


def record_from_microphone(duration: int = 5) -> bytes:
    """从麦克风录制音频（需要 pygame）。"""
    try:
        import pygame
        import pygame.mixer

        pygame.mixer.init(frequency=16000, size=-16, channels=1, buffer=4096)
        # 使用系统默认麦克风录制
        # 注意：此功能依赖系统音频配置
        print(f"[录音] 正在从麦克风录制 {duration} 秒...")
        print("[提示] 如果麦克风不可用，请将测试音频放入 test_audio/ 目录")

        # 简单录制方案（使用 pygame 的录音功能）
        # 如果 pygame 录音不可用，使用文件模式
        raise NotImplementedError("请使用文件模式测试")

    except Exception as e:
        print(f"[录音] 麦克风不可用: {e}")
        return b""


def load_test_audio() -> bytes:
    """从 test_audio/ 目录加载测试音频文件。"""
    if not TEST_AUDIO_DIR.exists():
        TEST_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[提示] 请将测试音频文件（WAV/MP3）放入: {TEST_AUDIO_DIR}")
        return b""

    for f in TEST_AUDIO_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in (".wav", ".mp3", ".ogg"):
            print(f"[加载] {f.name}")
            return f.read()

    print("[提示] 未找到测试音频文件，请放入 WAV/MP3 文件")
    return b""


async def test_text_mode():
    """测试文本对话模式。"""
    print("\n=== 文本对话测试 ===")
    print(f"连接到: {SERVER_URL}")
    async with websockets.connect(SERVER_URL) as ws:
        while True:
            user_input = input("\n你: ").strip()
            if not user_input:
                continue
            if user_input.upper() == "QUIT":
                break

            await ws.send(user_input)

            while True:
                msg = await ws.recv()
                try:
                    data = json.loads(msg)
                    if data.get("type") == "text_reply":
                        print(f"AI: {data['text']}")
                        break
                except (json.JSONDecodeError, TypeError):
                    pass


async def test_voice_mode():
    """测试语音交互模式。"""
    print("\n=== 语音交互测试 ===")

    audio_data = load_test_audio()
    if not audio_data:
        print("[跳过] 无测试音频，切换到文本模式")
        await test_text_mode()
        return

    print(f"连接到: {SERVER_URL}")
    async with websockets.connect(SERVER_URL) as ws:
        print(f"[发送] 音频数据: {len(audio_data)} bytes")
        await ws.send(audio_data)

        while True:
            msg = await ws.recv()
            try:
                data = json.loads(msg)
                if data.get("type") == "stt_result":
                    print(f"[STT] 你说: {data['text']}")
                elif data.get("type") == "text_reply":
                    print(f"[AI] {data['text']}")
                elif data.get("type") == "info":
                    print(f"[信息] {data['message']}")
            except (json.JSONDecodeError, TypeError):
                # 二进制音频数据
                if isinstance(msg, bytes):
                    print(f"[收到音频] {len(msg)} bytes")
                    # 保存回复音频
                    reply_path = TEST_AUDIO_DIR / "reply.wav"
                    with open(reply_path, "wb") as f:
                        f.write(msg)
                    print(f"[保存] 回复音频已保存到: {reply_path}")
                    break


async def main():
    print("数字人语音测试客户端")
    print("=" * 40)
    print("1. 文本对话测试")
    print("2. 语音交互测试")
    print("3. 退出")

    choice = input("\n请选择 (1/2/3): ").strip()

    if choice == "1":
        await test_text_mode()
    elif choice == "2":
        await test_voice_mode()
    else:
        print("已退出。")


if __name__ == "__main__":
    asyncio.run(main())
