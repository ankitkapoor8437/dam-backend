# Use an official Python runtime as a parent image
# python:3.10-slim usually has a recent enough sqlite3 for ChromaDB
FROM python:3.10-slim

# Set environment variables
# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
# Set a custom DATA_DIR if we want to use a volume (e.g. /data)
ENV DATA_DIR=/data

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
# build-essential for compiling some python packages
# sqlite3 just in case
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Create data directory
RUN mkdir -p /data/images /data/db

# Expose port (Render sets PORT env var, but we default to 8000)
EXPOSE 8000

# Run the application
# Use sh -c to expand the PORT variable (Render sets this)
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"
