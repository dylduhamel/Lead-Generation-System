FROM python:3.9.19-slim

WORKDIR /app

COPY requirements.txt .

# Install Python packages without cache
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set correct PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Create a non-root user with a home directory and set permissions
RUN useradd -u 1001 -m -s /bin/bash nonroot && \
    chown -R nonroot:nonroot /app

USER nonroot

CMD [ "python3", "src/send_email.py" ]