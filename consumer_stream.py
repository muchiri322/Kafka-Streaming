
import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

# Create Spark session
spark = SparkSession.builder \
    .appName("KafkaWeatherConsumer") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Define schema for weather JSON
schema = StructType().add("name", StringType()).add("main", StructType().add("temp", DoubleType()))

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "weather") \
    .option("startingOffsets", "latest") \
    .load()

# Parse the value from Kafka
weather_df = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.name", "data.main.temp")

# Write to console
query = weather_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
