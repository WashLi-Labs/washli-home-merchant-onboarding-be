# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any are needed for mysqlclient or others, though aiomysql is pure python mostly, sometimes cryptography needs build deps)
# installing git just in case, and cleaning up to keep image small
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port (Optional: EXPOSE doesn't handle $PORT well in some builders, but it's okay)
EXPOSE 10000

# Define environment variable for unbuffered output
ENV PYTHONUNBUFFERED=1

# Run the application
# We use the shell form (no brackets) or "sh -c" to allow $PORT expansion
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
