"""语音转文字 (STT) - 使用本地 Whisper 模型。"""

import whisper
from typing import Optional

_model: Optional[whisper.Whisper] = None
_model_size: Optional[str] = None


def _get_model(model_size: str = "base") -> whisper.Whisper:
    """懒加载 Whisper 模型（单例，支持切换模型大小）。"""
    global _model, _model_size
    if _model is None or _model_size != model_size:
        print(f"[STT] 正在加载 Whisper 模型: {model_size} ...")
        _model = whisper.load_model(model_size)
        _model_size = model_size
        print("[STT] Whisper 模型加载完成。")
    return _model


def transcribe(audio_bytes: bytes, model_size: str = "base") -> str:
    """将音频二进制数据转换为文字。

    Args:
        audio_bytes: 音频字节数据（支持 WAV/MP3/PCM 等 Whisper 支持的格式）。
        model_size: Whisper 模型大小。

    Returns:
        识别出的文字字符串。
    """
    try:
        import tempfile
        import os

        model = _get_model(model_size)

        # 写入临时文件让 Whisper 解码
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            result = model.transcribe(tmp_path, language="zh")
            text = result.get("text", "").strip()
        finally:
            os.unlink(tmp_path)

        if not text:
            print("[STT] 未识别出文字内容。")
        return text

    except Exception as e:
        print(f"[STT] 语音识别失败: {e}")
        return ""
