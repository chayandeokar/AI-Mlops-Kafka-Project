from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from jinja2 import Template
from kafka import KafkaProducer, KafkaConsumer
import threading
import asyncio

app = FastAPI()

# Kafka setup
producer = KafkaProducer(bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092")
consumer = KafkaConsumer("classification_result", group_id="result_group", bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092")

classification_result = ""

# Function to consume classification results
def consume_results():
    global classification_result
    for msg in consumer:
        classification_result = msg.value.decode("utf-8")

# Run Kafka consumer in a separate thread
thread = threading.Thread(target=consume_results, daemon=True)
thread.start()

# TailwindCSS Styled HTML Template
html_template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Classifier</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white flex items-center justify-center min-h-screen">

    <div class="bg-gray-800 p-6 rounded-xl shadow-lg w-full max-w-md text-center">
        <h1 class="text-3xl font-bold text-blue-400">Image Classifier</h1>
        <p class="text-gray-400 mt-2">Upload an image and get the classification result instantly!</p>

        <form action="/upload/" enctype="multipart/form-data" method="post" class="mt-6">
            <label class="block text-gray-300 text-sm mb-2">Select an image:</label>
            <input type="file" name="file" class="block w-full text-sm text-gray-400 bg-gray-700 p-2 rounded-md border border-gray-600">
            <button type="submit" class="mt-4 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-md w-full transition-all duration-300">Upload</button>
        </form>

        <div class="mt-6">
            <h2 class="text-lg font-semibold text-gray-300">Classification Result:</h2>
            <p class="text-2xl font-bold text-green-400 mt-2">{{ result }}</p>
        </div>
    </div>

</body>
</html>
""")

@app.get("/", response_class=HTMLResponse)
async def home():
    return html_template.render(result=classification_result)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    global classification_result
    image_data = await file.read()
    producer.send("image_upload", image_data)

    # Wait for the Kafka consumer to process the image
    for _ in range(10):  # Try for 10 seconds
        await asyncio.sleep(1)
        if classification_result:  # Check if result is updated
            break

    return HTMLResponse(html_template.render(result=classification_result))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
