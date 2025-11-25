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

# Copy source files
COPY lj_benchmark.c .
COPY Makefile .

# Build the benchmark
RUN make

# Default command runs the speed test
CMD ["make", "test-speed"]
