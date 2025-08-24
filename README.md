# Weather Data Streaming with Kafka

A real-time weather data streaming application that fetches weather information for Nairobi and London, then streams it using Apache Kafka for real-time processing and consumption.

## Overview
This project demonstrates a real-time data pipeline for collecting, processing, and displaying weather data.
It consists of two main components:
- **Producer** (`weather_prod.py`): Fetches weather data from OpenWeatherMap API and publishes to Kafka
- **Consumer** (`weather_con.py`): Consumes weather data from Kafka and displays it in real-time

## Architecture

```
OpenWeatherMap API → Producer → Kafka Topic → Consumer → Console Output
```

The system fetches weather data every 8 seconds for:
- Nairobi, Kenya (KE)
- Niger

## Prerequisites

### Software Requirements
- Python 3.7+
- Apache Kafka 2.8+
- Apache Zookeeper (required for Kafka)

### Python Dependencies
```bash
pip install kafka-python requests
```

## Setup Instructions

### 1. Start Kafka Infrastructure

First, start Zookeeper:
```bash
# Navigate to your Kafka installation directory
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Then start Kafka server:
```bash
bin/kafka-server-start.sh config/server.properties
```

### 2. Create Kafka Topic

Create the required topic:
```bash
bin/kafka-topics.sh --create --topic weather-nairobi-uk --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

Verify topic creation:
```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 3. Configure API Key
```

**Note**:Use your own API key from [OpenWeatherMap](https://openweathermap.org/api).

## Running the Application

### Start the Consumer
In one terminal, run the consumer to listen for incoming weather data:
```bash
python weather_con.py
```

You should see:
```
Listening for weather data...
```

### Start the Producer
In another terminal, run the producer to start fetching and streaming weather data:
```bash
python weather_prod.py
```

The producer will start fetching weather data every 30 seconds and you'll see output like:
```
Produced: {'city': 'Lusaka', 'country': 'KE', 'timestamp': 1733123456, 'temperature': 22.5, 'description': 'clear sky'}
Produced: {'city': 'Nairobi', 'country': 'GB', 'timestamp': 1733123456, 'temperature': 8.3, 'description': 'overcast clouds'}
```

### Consumer Output
The consumer will display formatted weather information:
```
Nairobi, KE - Clear sky at 22.5°C
London, GB - Overcast clouds at 8.3°C
```

## Configuration Options

### Producer Configuration
- **Fetch Interval**: Modify `time.sleep(30)` to change how often weather data is fetched
- **Cities**: Add or modify cities in the `cities` list
- **API Key**: Replace with your own OpenWeatherMap API key
- **Kafka Server**: Change `bootstrap_servers` if using a different Kafka setup

### Consumer Configuration
- **Topic**: Currently listening to `weather-nairobi-uk`
- **Offset Reset**: Set to `earliest` to read all messages from the beginning
- **Auto Commit**: Enabled for automatic offset management

## Data Format

The weather data structure sent through Kafka:
```json
{
    "city": "Nairobi",
    "country": "KE",
    "timestamp": 1733123456,
    "temperature": 22.5,
    "description": "clear sky"
}
```

## Troubleshooting

### Common Issues

1. **Kafka Connection Error**
   - Ensure Kafka and Zookeeper are running
   - Check if the correct ports (9092) are being used
   - Verify topic exists

2. **API Rate Limiting**
   - OpenWeatherMap free tier has rate limits
   - Consider increasing the fetch interval if you hit limits

3. **Import Errors**
   - Install required packages: `pip install kafka-python requests`

4. **No Data in Consumer**
   - Ensure producer is running and successfully fetching data
   - Check that both producer and consumer use the same topic name
   - Verify Kafka topic exists and is accessible

### Monitoring

You can monitor the Kafka topic using built-in tools:
```bash
# List consumer groups
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

# Check consumer group details
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group <group-id>
```

## Extending the Application

### Adding More Cities
Modify the `cities` list in `weather_prod.py`:
```python
cities = [
    ("Nairobi", "KE"),
    ("London", "GB"),
    ("New York", "US"),
    ("Tokyo", "JP")
]
```

### Adding More Weather Parameters
Extend the data structure to include additional weather information:
```python
return {
    "city": city,
    "country": country,
    "timestamp": int(time.time()),
    "temperature": response_data['main']['temp'],
    "humidity": response_data['main']['humidity'],
    "pressure": response_data['main']['pressure'],
    "description": response_data['weather'][0]['description']
}
```

## Security Considerations

- Store API keys in environment variables instead of hardcoding
- Use SSL/TLS for Kafka in production environments
- Implement proper authentication and authorization for Kafka clusters
- Consider using Kafka Connect for production data ingestion

## License

This project is provided for educational  purposes.
##conclusion
This project demonstrates how to build a real-time data pipeline using modern big data tools. With minimal setup, you can monitor weather data in real time and lay the foundation for more complex data engineering workflows.
