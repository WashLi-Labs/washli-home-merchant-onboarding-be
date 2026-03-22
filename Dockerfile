# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# We keep build-essential only if any dependencies need to be compiled
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Defined in Render environment, but fallback to 10000 for local testing
ENV PORT=10000

# Define environment variable for unbuffered output
ENV PYTHONUNBUFFERED=1

# Run the application using the dynamic PORT
# We use the shell form to allow $PORT expansion
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]