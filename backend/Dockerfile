# FROM python:3.11-slim

# WORKDIR /app

# RUN apt-get update && apt-get install -y --no-install-recommends netcat && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# ENV PYTHONUNBUFFERED=1

# EXPOSE 5000

# CMD ["./start.sh"]
# ====================
FROM python:3.10-slim
WORKDIR /app

# Install netcat for start.sh wait loop (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source (do NOT copy .env)
COPY . /app

# Ensure start script executable
RUN chmod +x start.sh

EXPOSE 5000

# Use start.sh to set up and run the app
CMD ["./start.sh"]
