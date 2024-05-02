# Use a Python 3.8 slim base image for the build stage
FROM python:3.8-slim AS builder

# Set working directory
WORKDIR /PAapp

# Copy only the requirements file to optimize caching
COPY requirements.txt .

# Install required packages for building dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libgomp1 \
        && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Use a lightweight base image for the runtime stage
FROM python:3.8-slim

# Set working directory
WORKDIR /PAapp

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

# Copy the rest of the application code
COPY . .
EXPOSE 5003
# Set PYTHONPATH environment variable
ENV PYTHONPATH /NBapp

# Run the application
CMD ["python", "app.py"]