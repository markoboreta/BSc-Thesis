FROM python:3.11-slim AS builder
WORKDIR /NBapp
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /NBapp
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .
EXPOSE 5002
# Set PYTHONPATH environment variable
ENV PYTHONPATH /NBapp

# Run the application
CMD ["python", "app.py"]