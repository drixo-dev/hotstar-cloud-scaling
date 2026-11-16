FROM python:3.12-slim

WORKDIR /app

# Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# t3.micro has 2 vCPUs. Set WORKERS=2 so all available cores are utilized under load.
ENV WORKERS=2

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 --workers ${WORKERS}"]
