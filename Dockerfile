# Use official Python runtime as a base image
FROM python:3.11-slim

# Ensure stdout and stderr are unbuffered
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install system dependencies (if you later use psycopg2, uncomment libpq-dev)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# If you need migrations, you can run:
# RUN alembic upgrade head

# Default command to run the bot
CMD ["python", "-m", "vpnsellbot.main"]
