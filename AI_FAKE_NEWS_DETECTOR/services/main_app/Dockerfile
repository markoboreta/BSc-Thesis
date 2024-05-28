# image for docker to build
FROM python:3.11-slim AS builder
WORKDIR /mainapp
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /mainapp
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .
ENV PYTHONPATH /mainapp

# Expose the Flask app port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]