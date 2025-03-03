FROM python:3.11.11-slim

# 删除旧配置（如有）
RUN rm -f /etc/apt/sources.list.d/*.sources

# 添加新镜像源到 sources.list
RUN echo "deb http://mirrors.aliyun.com/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn

EXPOSE 9091

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=9091", "--server.address=0.0.0.0"]