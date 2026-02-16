from kafka import KafkaConsumer
import json
import pandas as pd
from collections import defaultdict
from datetime import datetime
import os

print("=" * 50)
print("Batch Processor Started!")
print("Processing events from Kafka...")
print("=" * 50)

# Connect to Kafka
consumer = KafkaConsumer(
    'ecommerce-events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    consumer_timeout_ms=10000
)

# Store all events and metrics
all_events = []
event_counts = defaultdict(int)
product_metrics = defaultdict(lambda: {'count': 0, 'total_price': 0})
device_counts = defaultdict(int)
total_events = 0

print("\nReading messages from Kafka...\n")

# Process messages
for message in consumer:
    event = message.value
    all_events.append(event)
    total_events += 1
    
    # Count by event type
    event_counts[event['event_type']] += 1
    
    # Product metrics
    product = event['product']
    product_metrics[product]['count'] += 1
    product_metrics[product]['total_price'] += event['price']
    
    # Device counts
    device_counts[event['device']] += 1
    
    if total_events % 10 == 0:
        print(f"Processed {total_events} events...")

consumer.close()

# Display results
print("\n" + "=" * 50)
print(f"TOTAL EVENTS PROCESSED: {total_events}")
print("=" * 50)

print("\n--- EVENT COUNTS BY TYPE ---")
for event_type, count in sorted(event_counts.items()):
    print(f"{event_type:15} {count:5} events")

print("\n--- PRODUCT METRICS ---")
print(f"{'Product':<15} {'Count':<8} {'Avg Price':<12} {'Total Revenue':<15}")
print("-" * 55)
for product, metrics in sorted(product_metrics.items()):
    avg_price = metrics['total_price'] / metrics['count']
    print(f"{product:<15} {metrics['count']:<8} ${avg_price:<11.2f} ${metrics['total_price']:<14.2f}")

print("\n--- DEVICE STATISTICS ---")
for device, count in sorted(device_counts.items()):
    print(f"{device:10} {count:5} events")

# Save to structured formats
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# 1. Save raw events as CSV
df_events = pd.DataFrame(all_events)
csv_file = f"../data/raw_events_{timestamp}.csv"
df_events.to_csv(csv_file, index=False)
print(f"\n✓ Raw events saved to CSV: {csv_file}")

# 2. Save raw events as Parquet
parquet_file = f"../data/raw_events_{timestamp}.parquet"
df_events.to_parquet(parquet_file, index=False)
print(f"✓ Raw events saved to Parquet: {parquet_file}")

# 3. Save aggregated product metrics as CSV
product_data = []
for product, metrics in product_metrics.items():
    product_data.append({
        'product': product,
        'total_events': metrics['count'],
        'avg_price': round(metrics['total_price'] / metrics['count'], 2),
        'total_revenue': round(metrics['total_price'], 2)
    })
df_products = pd.DataFrame(product_data)
product_csv = f"../data/product_metrics_{timestamp}.csv"
df_products.to_csv(product_csv, index=False)
print(f"✓ Product metrics saved to CSV: {product_csv}")

# 4. Save event counts as CSV
event_data = [{'event_type': k, 'count': v} for k, v in event_counts.items()]
df_event_counts = pd.DataFrame(event_data)
even