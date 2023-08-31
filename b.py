import random
import asyncio
from confluent_kafka import Consumer

class KafkaListener:
    def __init__(self, bootstrap_servers: str, topic: list[str], offset: str = 'earliest') -> None:
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': self.__create_random_string(10),
            'auto.offset.reset': offset
        })
        self.consumer.subscribe(topic)

    def __create_random_string(self, length: int) -> str:
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(random.choice(characters) for _ in range(length))
    
    def listen(self, poll_timing: float = 1.0) -> None:
        while True:
            message = self.consumer.poll(poll_timing)

            if message is None:
                continue
            if message.error():
                print("Consumer error: {}".format(message.error()))
                continue

            key = message.key()
            value = message.value()
            headers = message.headers()

            if key is not None and len(key) > 0:
                print(f'Received message key: {key}')

            if value is not None:
                value_decoded = value.decode('utf-8')
                if len(value_decoded) > 0:
                    print(f'Received message value: {value_decoded}')

            if headers is not None:
                for key, value in headers.items():
                    print('Key: {} Value: {}'.format(key, value))
    
def run() -> None:
    bootstrap_servers = "localhost:9092"
    topic = ["example"]

    listener = KafkaListener(bootstrap_servers, topic)
    asyncio.run(listener.listen())

if __name__ == "__main__":
    run()
