"""文字转语音 (TTS) - 使用 gTTS。"""

from io import BytesIO
from typing import Optional
from gtts import gTTS


def synthesize(text: str, lang: str = "zh") -> bytes:
    """将文本转换为 MP3 音频字节。

    Args:
        text: 要转换的文本。
        lang: 语言代码（zh=中文, en=英文）。

    Returns:
        MP3 格式的音频字节数据。
    """
    if not text or not text.strip():
        print("[TTS] 输入文本为空，返回空音频。")
        return b""

    try:
        tts = gTTS(text=text, lang=lang)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        audio_bytes = buf.read()
        print(f"[TTS] 合成完成，音频大小: {len(audio_bytes)} bytes")
        return audio_bytes
    except Exception as e:
        print(f"[TTS] 语音合成失败: {e}")
        return b""
