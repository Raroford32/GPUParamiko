# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.4.0-base-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install the SSH_GPU package
RUN pip3 install -e .

# Expose SSH port
EXPOSE 22

# Set entry point
CMD ["python3", "-m", "ssh_gpu.server"]
