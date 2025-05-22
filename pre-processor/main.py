import cv2
import numpy as np
from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer("image_upload", group_id="image_group", bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092")
producer = KafkaProducer(bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092")

def preprocess_image(image_bytes):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))
    img = img.astype("float32") / 255.0
    return img.tobytes()

for msg in consumer:
    processed_image = preprocess_image(msg.value)
    producer.send("image_preprocessed", processed_image)
