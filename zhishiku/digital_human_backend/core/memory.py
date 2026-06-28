"""对话记忆管理。"""

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


class SessionMemory:
    """基于内存的会话记忆，支持多轮对话。"""

    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self.history = ChatMessageHistory()

    def add_user_message(self, message: str) -> None:
        self.history.add_user_message(message)
        self._trim()

    def add_ai_message(self, message: str) -> None:
        self.history.add_ai_message(message)
        self._trim()

    def get_messages(self):
        """返回当前所有消息。"""
        return self.history.messages

    def get_context_string(self) -> str:
        """将历史消息格式化为上下文字符串。"""
        lines = []
        for msg in self.history.messages:
            role = "用户" if isinstance(msg, HumanMessage) else "助手"
            lines.append(f"{role}: {msg.content}")
        return "\n".join(lines)

    def clear(self) -> None:
        self.history.clear()

    def _trim(self) -> None:
        """保留最近 max_history 条消息。"""
        msgs = self.history.messages
        if len(msgs) > self.max_history:
            self.history.messages = msgs[-self.max_history:]
