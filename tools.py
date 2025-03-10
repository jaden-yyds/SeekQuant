# 自定义回调处理器
import asyncio
import queue
import threading
from collections.abc import AsyncIterator
from typing import Tuple, Generator, Any, TypeVar

T = TypeVar('T')
def split_async_generator(
    async_iter: AsyncIterator[T]
) -> tuple[Generator[T, None, None], Generator[T, None, None]]:
    # 创建两个队列用于存储数据
    queue1 = queue.Queue()
    queue2 = queue.Queue()
    # 事件循环和终止信号
    loop = asyncio.new_event_loop()
    stopped = threading.Event()

    # 异步消费函数
    async def _consume():
        try:
            async for item in async_iter:
                queue1.put(item)  # 推送到队列1
                queue2.put(item)  # 推送到队列2
        except Exception as e:
            # 异常处理（可选）
            pass
        finally:
            # 发送终止信号
            queue1.put(None)
            queue2.put(None)
            stopped.set()  # 标记异步迭代已结束

    # 在独立线程中运行异步事件循环
    def _run_loop():
        loop.run_until_complete(_consume())
        loop.close()

    thread = threading.Thread(target=_run_loop)
    thread.daemon = True  # 设置为守护线程
    thread.start()

    # 生成器定义（核心逻辑）
    def _generator(q: queue.Queue) -> Generator[T, None, None]:
        while True:
            # 如果异步迭代已结束且队列为空，则终止
            if stopped.is_set() and q.empty():
                break
            item = q.get()
            if item is None:  # 终止信号
                break
            yield item  # 实时生成数据

    # 返回两个生成器
    return _generator(queue1), _generator(queue2)