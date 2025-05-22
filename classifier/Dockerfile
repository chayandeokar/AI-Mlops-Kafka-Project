FROM python:3.9-alpine

WORKDIR /app

# Install system dependencies for image processing
RUN apk add --no-cache opencv tesseract-ocr

# Install required Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the classification logic
COPY . .

# Expose relevant ports (optional)
EXPOSE 5002

# Run the classifier microservice
CMD ["python", "main.py"]
