import json
import time
import requests
from kafka import KafkaProducer

cities = ["Nairobi", "Niger", "Pretoria", "Lusaka", "Lagos", "Cairo"]
API_KEY = "8f7c039d18fc20fade3dcca7a8fe1693"
KAFKA_TOPIC = "weather_data"
KAFKA_SERVER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

while True:
    for city in cities:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            data["city"] = city
            producer.send(KAFKA_TOPIC, value=data)
            print(f"Sent weather data for {city}")
        except Exception as e:
            print(f"Error fetching/sending data for {city}: {e}")
    time.sleep(480))  # wait 8 minutes