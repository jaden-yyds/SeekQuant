import os
from langchain_deepseek import ChatDeepSeek

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
