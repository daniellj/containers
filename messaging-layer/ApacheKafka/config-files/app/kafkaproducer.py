from datetime import datetime
from confluent_kafka import Producer
import socket


if __name__ == "__main__":
    hostname = socket.gethostname()
    hostserver = "kafka"

    host = hostname if hostname == hostserver else "127.0.0.1"

    conf = {
     "bootstrap.servers": f"{host}:9092, {host}:9093, {host}:9094"
    }

    topic = "topic01"
    # number of messages to send
    numberOfRecords = 2000

    # Create Producer instance
    producer = Producer(**conf)
    delivered_records = 0

    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently failed delivery after retries.
    def acked(err, msg):
        global delivered_records
        """Delivery report handler called on successful or failed delivery of message """
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            delivered_records += 1
            print("Produced record to topic {} partition [{}] @ offset {}".format(msg.topic(), msg.partition(), msg.offset()))

    for n in range(numberOfRecords):
        record_key = "messageKey " + str(n)
        record_value = "messageValue " + str(n) + " at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
        print("Producing record: {}\t{}".format(record_key, record_value))
        producer.produce(topic, key=record_key, value=record_value, on_delivery=acked)
        # p.poll() serves delivery reports (on_delivery) from previous produce() calls.
        producer.poll(0)

    # Synchronous writes
    producer.flush()
    print("{} messages were produced to topic {}!".format(delivered_records, topic))