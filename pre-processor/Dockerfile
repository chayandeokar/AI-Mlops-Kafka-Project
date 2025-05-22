# Use Alpine-based Python image
FROM python:3.9-alpine

# Install system dependencies required for OpenCV
RUN apk add --no-cache \
    gcc \
    g++ \
    make \
    cmake \
    ninja \
    musl-dev \
    linux-headers \
    libjpeg-turbo-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    libwebp-dev \
    tiff-dev \
    openblas-dev \
    harfbuzz-dev \
    fribidi-dev

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the port (assuming FastAPI runs on 8000)
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
