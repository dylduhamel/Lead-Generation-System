# Stage 1: Build Stage
FROM python:3.9.19-slim as builder

WORKDIR /app

COPY containers/scraping/requirements.txt .

# Install Python packages without cache
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome and other dependencies
RUN apt-get update && apt-get install -y wget unzip gnupg curl && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && apt-get install -y google-chrome-stable


# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/ && \
    unzip ~/chromedriver_linux64.zip -d ~/ && \
    rm ~/chromedriver_linux64.zip && \
    mv -f ~/chromedriver /usr/local/bin/chromedriver && \
    chown root:root /usr/local/bin/chromedriver && \
    chmod 0755 /usr/local/bin/chromedriver


# Stage 2: Runtime Stage
FROM python:3.9.19-slim

WORKDIR /app

# Copy only necessary files from builder stage
COPY --from=builder /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=builder /usr/bin/google-chrome /usr/bin/google-chrome
COPY --from=builder /usr/lib /usr/lib 
COPY containers/scraping/src/ ./src
COPY containers/scraping/scrapers/ ./scrapers
COPY utils ./utils

# Set correct PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN useradd -u 1001 -m -s /bin/bash nonroot && \
    mkdir -p /home/nonroot && \
    chown -R nonroot:nonroot /home/nonroot /app

USER nonroot

CMD [ "python3", "src/scrape.py" ]
