# Use slim Python base image
FROM python:3.11-slim

# Install system-level dependencies: Tesseract OCR, Poppler, ZBar
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libzbar0 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies first (layer caching)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ .

# Copy frontend (served as static files by FastAPI)
COPY frontend/ ../frontend/

# Expose port
EXPOSE 8080

# Start the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
