# Stage 1: Build Stage
FROM python:3.9.19-slim as builder

WORKDIR /app

COPY requirements.txt .

# Install Python packages without cache
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome and other dependencies
RUN apt-get update && apt-get install -y wget unzip gnupg && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && apt-get install -y google-chrome-stable

# Stage 2: Runtime Stage
FROM python:3.9.19-slim

WORKDIR /app

# Copy only necessary files from builder stage
COPY --from=builder /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=builder /usr/bin/google-chrome /usr/bin/google-chrome
COPY --from=builder /usr/lib /usr/lib 
COPY src/ ./src
COPY scrapers/ ./scrapers
COPY utils/ ./utils

# Set correct PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Create a non-root user with a home directory and set permissions
RUN useradd -u 1001 -m -s /bin/bash nonroot && \
    chown -R nonroot:nonroot /app

USER nonroot

CMD [ "python3", "src/scrape.py" ]
