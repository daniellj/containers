from confluent_kafka import Consumer
import socket


if __name__ == '__main__':
    topic = "topic01"
    hostname = socket.gethostname()
    hostserver = "kafka"

    host = hostname if hostname == hostserver else "127.0.0.1"

    conf = {
     "bootstrap.servers": f"{host}:9092, {host}:9093, {host}:9094"
     ,'group.id': f"{topic}",
    }

    # Create Consumer instance
    consumer = Consumer(conf)

    # Subscribe to topic
    consumer.subscribe([topic])

    # Process messages
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # No message available within timeout.
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print('error: {}'.format(msg.error()))
            else:
                # Check for Kafka message
                record_key = "Null" if msg.key() is None else msg.key().decode('utf-8')
                record_value = msg.value().decode('utf-8')
                print("Consumed record with key "+ record_key + " and value " + record_value)
    except KeyboardInterrupt:
        pass
    finally:
        print("Leave group and commit final offsets")
        consumer.close()