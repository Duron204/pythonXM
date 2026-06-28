"""Agent 可调用的工具集合。"""

import json
import urllib.request
from typing import Optional
from langchain_core.tools import tool


@tool
def get_weather(city: str = "北京") -> str:
    """查询指定城市的当前天气信息。输入城市名称（中文），返回天气描述。"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        current = data.get("current_condition", [{}])[0]
        temp = current.get("temp_C", "未知")
        feels = current.get("FeelsLikeC", "未知")
        desc_list = current.get("lang_zh", [])
        desc = desc_list[0].get("value", "未知") if desc_list else current.get("weatherDesc", [{}])[0].get("value", "未知")
        humidity = current.get("humidity", "未知")
        return f"{city}当前天气：{desc}，温度 {temp}°C（体感 {feels}°C），湿度 {humidity}%"
    except Exception as e:
        return f"获取天气信息失败：{str(e)}。请检查网络连接或稍后重试。"


@tool
def send_notification(message: str, recipient: str = "管理员") -> str:
    """发送一条简单通知。在实际项目中可对接邮件/消息服务，当前为模拟实现。"""
    print(f"[通知] 发送给 {recipient}: {message}")
    return f"已向 {recipient} 发送通知：{message}"


@tool
def get_current_time() -> str:
    """获取当前日期和时间。"""
    from datetime import datetime
    now = datetime.now()
    return f"当前时间：{now.strftime('%Y年%m月%d日 %H:%M:%S')}"


# 工具列表 - 供 Agent 绑定
TOOLS = [get_weather, send_notification, get_current_time]
