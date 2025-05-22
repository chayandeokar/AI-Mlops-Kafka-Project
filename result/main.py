from fastapi import FastAPI
from kafka import KafkaConsumer
import threading

app = FastAPI()
consumer = KafkaConsumer("classification_result", group_id="result_group", bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092")

classification_result = ""

def consume_results():
    global classification_result
    for msg in consumer:
        classification_result = msg.value.decode("utf-8")

thread = threading.Thread(target=consume_results, daemon=True)
thread.start()

@app.get("/result/")
def get_result():
    return {"classification": classification_result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
