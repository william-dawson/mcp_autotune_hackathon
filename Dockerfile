FROM ubuntu:22.04

# Avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    valgrind \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install fastmcp

# Set working directory
WORKDIR /app

# Copy all source files
COPY lj_benchmark.c .
COPY Makefile .
COPY server.py .
COPY async_api.py .
COPY run.py .

# Default command runs the MCP server
CMD ["python3", "server.py"]
