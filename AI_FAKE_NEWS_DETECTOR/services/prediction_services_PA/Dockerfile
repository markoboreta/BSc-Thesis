FROM python:3.11-slim AS builder
# Set working directory
WORKDIR /PAapp
COPY requirements.txt .
# Install required packages for building dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /PAapp
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .
EXPOSE 5003
# Set PYTHONPATH environment variable
ENV PYTHONPATH /PAapp

# Run the application
CMD ["python", "app.py"]