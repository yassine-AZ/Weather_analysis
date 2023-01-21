from kafka import KafkaProducer
import json

class Producer:

    kafka_bootstrap_server = "localhost:9092"
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server,
        api_version=(0,10),
        value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    @classmethod
    def sendData(self,topic,data):
        self.producer.send(topic,data)
        self.producer.flush()
        print("publish msg")
        

    @classmethod
    def flushData(self):
        self.producer.flush()
        print("publish msg")
