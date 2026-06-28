"""Agent 模块 - 集成 RAG 检索 + 工具调用的智能对话代理。"""

from typing import Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from config.settings import get_llm
from core.tools import TOOLS
from core.memory import SessionMemory
from core.rag_chain import query_rag


SYSTEM_PROMPT = """你是一个数字人的智能大脑，具备以下能力：
1. 基于知识库回答问题（当用户的问题涉及知识库内容时使用检索功能）。
2. 调用工具完成任务（如查询天气、发送通知、获取时间等）。
3. 日常闲聊和对话。

请根据用户的问题，判断应该：
- 直接用自身知识回答（闲聊、常识性问题）
- 调用知识库检索回答（专业性问题、项目相关问题）
- 调用工具完成（需要查询天气、时间等具体操作）

请用中文简洁地回答。"""


class DigitalHumanAgent:
    """数字人 Agent - 简化版路由逻辑，适配本地模型。"""

    def __init__(self):
        self.llm = get_llm(temperature=0.7)
        self.memory = SessionMemory(max_history=20)
        self.tools_map = {t.name: t for t in TOOLS}
        self._has_vector_store = False

        # 尝试检测向量库是否可用
        try:
            from config.settings import VECTOR_STORE_PATH
            import os
            self._has_vector_store = os.path.exists(VECTOR_STORE_PATH)
        except Exception:
            self._has_vector_store = False

    def chat(self, user_input: str) -> str:
        """处理用户输入，返回回复文本。

        简化路由逻辑：
        1. 先尝试判断是否需要工具调用
        2. 再尝试 RAG 检索
        3. 最后直接 LLM 对话
        """
        self.memory.add_user_message(user_input)

        # 第一步：用 LLM 判断用户意图
        intent = self._classify_intent(user_input)

        response = ""

        if intent == "tool":
            # 工具调用路径
            response = self._handle_tool_call(user_input)
        elif intent == "rag" and self._has_vector_store:
            # RAG 检索路径
            response = self._handle_rag(user_input)
        else:
            # 直接对话路径
            response = self._handle_direct_chat(user_input)

        self.memory.add_ai_message(response)
        return response

    def _classify_intent(self, user_input: str) -> str:
        """用 LLM 判断用户意图：tool / rag / chat。"""
        messages = [
            SystemMessage(content="你是一个意图分类器。根据用户输入，只回复以下其中一个词：tool、rag、chat。\n"
                         "- tool：用户想要查询天气、时间、发通知等需要工具的操作\n"
                         "- rag：用户询问专业知识、文档内容、项目相关问题\n"
                         "- chat：日常问候、闲聊、简单问答"),
            HumanMessage(content=user_input),
        ]
        try:
            result = self.llm.invoke(messages)
            intent = result.content.strip().lower()
            if intent in ("tool", "rag", "chat"):
                return intent
        except Exception as e:
            print(f"[Agent] 意图分类失败: {e}")
        return "chat"

    def _handle_tool_call(self, user_input: str) -> str:
        """处理工具调用 - 让 LLM 输出工具调用意图，解析后实际执行工具。"""
        tool_descriptions = "\n".join(
            f"- {name}: {t.description}" for name, t in self.tools_map.items()
        )
        dispatch_prompt = (
            "你是一个工具调度助手。根据用户需求，从可用工具中选择一个并生成调用指令。\n"
            "必须严格按以下 JSON 格式输出，不要输出其他内容：\n"
            '{"tool": "工具名", "args": {"参数名": "参数值"}}\n\n'
            f"可用工具：\n{tool_descriptions}\n\n"
            "示例：用户问'北京天气' -> {\"tool\": \"get_weather\", \"args\": {\"city\": \"北京\"}}\n"
            "示例：用户问'现在几点了' -> {\"tool\": \"get_current_time\", \"args\": {}}"
        )
        messages = [
            SystemMessage(content=dispatch_prompt),
            HumanMessage(content=user_input),
        ]
        try:
            result = self.llm.invoke(messages)
            return self._parse_and_execute_tool(result.content)
        except Exception as e:
            return f"工具调用出错: {str(e)}"

    def _parse_and_execute_tool(self, llm_output: str) -> str:
        """解析 LLM 输出的工具调用指令并执行。"""
        import json

        # 尝试从 LLM 输出中提取 JSON
        text = llm_output.strip()
        # 去除可能的 markdown 代码块标记
        if text.startswith("```"):
            text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        text = text.strip()

        try:
            call = json.loads(text)
        except json.JSONDecodeError:
            # 如果 JSON 解析失败，尝试在文本中查找 JSON
            import re
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                try:
                    call = json.loads(match.group())
                except json.JSONDecodeError:
                    return f"无法解析工具调用指令: {text}"
            else:
                return f"无法解析工具调用指令: {text}"

        tool_name = call.get("tool", "")
        tool_args = call.get("args", {})

        if tool_name not in self.tools_map:
            return f"未知工具: {tool_name}，可用工具: {', '.join(self.tools_map.keys())}"

        try:
            tool_result = self.tools_map[tool_name].invoke(tool_args)
            return f"[工具结果] {tool_result}"
        except Exception as e:
            return f"工具执行失败 ({tool_name}): {str(e)}"

    def _handle_rag(self, user_input: str) -> str:
        """处理 RAG 检索问答。"""
        try:
            result = query_rag(user_input)
            answer = result.get("answer", "抱歉，检索未返回结果。")
            sources = result.get("sources", [])
            if sources:
                answer += "\n\n参考来源："
                for i, src in enumerate(sources[:3], 1):
                    meta = src.get("metadata", {})
                    source_name = meta.get("source", "未知来源")
                    answer += f"\n[{i}] {source_name}"
            return answer
        except Exception as e:
            return f"知识库检索出错: {str(e)}"

    def _handle_direct_chat(self, user_input: str) -> str:
        """直接 LLM 对话。"""
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            *self.memory.get_messages(),
        ]
        try:
            result = self.llm.invoke(messages)
            return result.content
        except Exception as e:
            return f"回复出错: {str(e)}"

    def _build_tool_prompt(self) -> str:
        tool_names = ", ".join(self.tools_map.keys())
        return (
            f"你是一个工具调度助手。可用工具：{tool_names}。\n"
            "请分析用户需求，输出 JSON 格式的工具调用指令。"
        )

    def reset(self) -> None:
        """重置会话记忆。"""
        self.memory.clear()
