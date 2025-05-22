import tensorflow as tf
import numpy as np
from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer("image_preprocessed", group_id="image_group", bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092")
producer = KafkaProducer(bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092")

model = tf.keras.applications.MobileNetV2(weights="imagenet")

def classify_image(image_bytes):
    img_array = np.frombuffer(image_bytes, dtype=np.float32).reshape((224, 224, 3))
    img_array = np.expand_dims(img_array, axis=0)
    preds = model.predict(img_array)
    label = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0][0][1]
    return label

for msg in consumer:
    label = classify_image(msg.value)
    producer.send("classification_result", label.encode("utf-8"))
