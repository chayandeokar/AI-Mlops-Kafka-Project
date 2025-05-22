from fastapi import FastAPI, UploadFile, File
from kafka import KafkaProducer
import uvicorn

app = FastAPI()
producer = KafkaProducer(bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    image_data = await file.read()
    producer.send("image_upload", image_data)
    return {"message": "Image uploaded successfully!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
