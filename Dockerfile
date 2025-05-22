# Use Python Alpine for a lightweight image
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV & Kafka
RUN apk add --no-cache gcc musl-dev libffi-dev \
    && apk add --no-cache jpeg-dev zlib-dev \
    && apk add --no-cache tiff-dev freetype-dev lcms2-dev \
    && apk add --no-cache openjpeg-dev libwebp-dev harfbuzz-dev \
    && apk add --no-cache fribidi-dev libxcb libpng \
    && apk add --no-cache git curl ffmpeg

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose port 8000
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "frontend:app", "--host", "0.0.0.0", "--port", "8000"]
