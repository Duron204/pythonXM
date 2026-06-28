"""音频格式转换辅助函数。"""

import struct
import tempfile
import os
from typing import Optional


def pcm_to_wav(pcm_data: bytes, sample_rate: int = 16000,
               channels: int = 1, sample_width: int = 2) -> bytes:
    """将原始 PCM 数据转换为 WAV 格式。

    Args:
        pcm_data: 原始 PCM 字节数据。
        sample_rate: 采样率。
        channels: 声道数。
        sample_width: 每个样本的字节数（1=8bit, 2=16bit）。

    Returns:
        WAV 格式的字节数据。
    """
    data_size = len(pcm_data)
    byte_rate = sample_rate * channels * sample_width

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        36 + data_size,
        b"WAVE",
        b"fmt ",
        16,  # PCM chunk size
        1,   # PCM format
        channels,
        sample_rate,
        byte_rate,
        channels * sample_width,
        sample_width * 8,
        b"data",
        data_size,
    )
    return header + pcm_data


def audio_bytes_to_wav_file(audio_bytes: bytes, suffix: str = ".wav") -> Optional[str]:
    """将音频字节保存为临时 WAV 文件，返回文件路径。"""
    try:
        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        tmp.write(audio_bytes)
        tmp.close()
        return tmp.name
    except Exception as e:
        print(f"[AudioUtils] 创建临时文件失败: {e}")
        return None


def cleanup_temp_file(path: Optional[str]) -> None:
    """删除临时文件。"""
    if path and os.path.exists(path):
        try:
            os.unlink(path)
        except Exception:
            pass
