from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

# Create Spark Session
spark = SparkSession.builder \
    .appName("EcommerceStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("=" * 50)
print("Spark Streaming Started!")
print("Reading from Kafka topic: ecommerce-events")
print("=" * 50)

# Define schema for incoming data
schema = StructType([
    StructField("event_id", StringType()),
    StructField("event_type", StringType()),
    StructField("user_id", StringType()),
    StructField("product", StringType()),
    StructField("price", DoubleType()),
    StructField("timestamp", StringType()),
    StructField("country", StringType()),
    StructField("device", StringType())
])

# Read from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ecommerce-events") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse JSON data
events = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Real-time aggregations
# 1. Count events by type
event_counts = events.groupBy("event_type").count()

# 2. Average price by product
product_metrics = events.groupBy("product").agg(
    count("*").alias("total_events"),
    avg("price").alias("avg_price"),
    sum("price").alias("total_revenue")
)

# 3. Events by device
device_stats = events.groupBy("device").count()

# Print to console
print("\n--- EVENT COUNTS BY TYPE ---")
query1 = event_counts.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

print("\n--- PRODUCT METRICS ---")
query2 = product_metrics.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

print("\n--- DEVICE STATISTICS ---")
query3 = device_stats.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

# Wait for termination
spark.streams.awaitAnyTermination()