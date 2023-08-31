import random
import asyncio
from typing import Optional
from kafka import KafkaConsumer

class KafkaListener:
    def __init__(self, bootstrap_servers: list[str], topic: str, group_id: str) -> None:
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True)

    async def listen(self) -> None:
        for message in self.consumer:
            key = message.key.decode("utf-8") if message.key is not None else ""
            value = message.value.decode("utf-8") if message.value is not None else ""
            headers = message.headers if message.headers is not None and len(message.headers) > 0 else None
            self.printValues(key, value, headers)

    def printValues(self, key: Optional[str], value: Optional[str], headers: Optional[list[str]]) -> None:
        print("Key:", key)
        print("Value:", value)
        if headers is not None:
            print("Headers:")
            [print(f"{header_key}: {header_value}") for header_key, header_value in headers.items()]

def create_random_string(length: int) -> str:
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(characters) for _ in range(length))

def run() -> None:
    bootstrap_servers = ["localhost:9092"]
    topic = "example"
    group_id = create_random_string(10)

    listener = KafkaListener(bootstrap_servers, topic, group_id)
    asyncio.run(listener.listen())

if __name__ == "__main__":
    run()