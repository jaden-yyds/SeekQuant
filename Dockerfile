FROM python:3.11.11-slim

WORKDIR /app

# 删除旧配置（如有）
RUN rm -f /etc/apt/sources.list.d/*.sources

# 添加新镜像源到 sources.list
RUN echo "deb http://mirrors.aliyun.com/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y build-essential curl software-properties-common && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn

EXPOSE 9091

HEALTHCHECK CMD curl --fail http://localhost:9091/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=9091", "--server.address=0.0.0.0"]