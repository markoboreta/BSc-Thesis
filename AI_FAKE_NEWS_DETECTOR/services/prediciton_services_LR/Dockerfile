# Use a Python 3.8 slim base image for the build stage
FROM python:3.11-slim AS builder
# Set working directory
WORKDIR /LRapp
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /LRapp
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH 
COPY . .
EXPOSE 5001
# Set PYTHONPATH environment variable
ENV PYTHONPATH /LRapp
CMD ["python", "app.py"]