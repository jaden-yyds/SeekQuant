import asyncio
import os
from collections.abc import AsyncIterator
from typing import Tuple
from langchain_core.messages import BaseMessageChunk
from langchain_deepseek import ChatDeepSeek
import tools

# 必须的环境变量检查
required_env_vars = ["DEEPSEEK_MODEL", "DEEPSEEK_API_KEY", "DEEPSEEK_API_BASE"]
missing_vars = [var for var in required_env_vars if var not in os.environ]
if missing_vars:
    raise ValueError(f"缺少必需的环境变量: {', '.join(missing_vars)}")

llm = ChatDeepSeek(
    model=os.environ["DEEPSEEK_MODEL"],
    temperature=float(os.environ.get("DEEPSEEK_TEMPERATURE", "0.7")),  # 默认温度0.7
    max_tokens=int(os.environ["DEEPSEEK_MAX_TOKENS"]) if "DEEPSEEK_MAX_TOKENS" in os.environ else None,
    timeout=int(os.environ["DEEPSEEK_TIMEOUT"]) if "DEEPSEEK_TIMEOUT" in os.environ else None,
    max_retries=int(os.environ.get("DEEPSEEK_MAX_RETRIES", "2")),     # 默认重试2次
    api_key=os.environ["DEEPSEEK_API_KEY"],
    api_base=os.environ["DEEPSEEK_API_BASE"],
)

def send_message(message: str):
    messages = [
        # (
        #     "system",
        #     "You are a helpful assistant that translates English to French. Translate the user sentence.",
        # ),
        ("human", message),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content

def async_send_message(message: str):
    messages = [
        ("human", message),
    ]
    return llm.astream(messages)

def async_chat_split_think_answer(message: str) -> Tuple[AsyncIterator[BaseMessageChunk], AsyncIterator[BaseMessageChunk]]:
    messages = [
        ("human", message),
    ]
    # 拆分为两个流
    ai_stream, human_stream = asyncio.run(tools.split_chat_stream(llm.astream(messages)))
    return ai_stream, human_stream

async def print_events(message: str):
    # 定义一个包含思考逻辑的链
    # chain = RunnableLambda(lambda x: "思考中...") | llm

    # 监听事件流
    async for event in llm.astream(message):
        print(event)
        # event_type = event["event"]
        # if "chat_model" in event_type:  # 模型处理阶段
        #     print(f"[Think] {event['name']}: {event['data'].get('kwargs', {})}")
        # elif "chain" in event_type:    # 回答生成阶段
        #     print(f"[Think] {event['name']}: {event['data'].get('kwargs', {})}")