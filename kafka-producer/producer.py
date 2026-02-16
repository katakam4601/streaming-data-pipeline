from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
from datetime import datetime

# Initialize
fake = Faker()
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Starting to send events to Kafka...")
print("Press Ctrl+C to stop")

# Event types
event_types = ['page_view', 'add_to_cart', 'purchase', 'search']
products = ['Laptop', 'Phone', 'Headphones', 'Watch', 'Camera', 'Tablet', 'Speaker', 'Monitor']

try:
    event_count = 0
    while True:
        # Generate fake event
        event = {
            'event_id': fake.uuid4(),
            'event_type': random.choice(event_types),
            'user_id': fake.uuid4()[:8],
            'product': random.choice(products),
            'price': round(random.uniform(50, 2000), 2),
            'timestamp': datetime.now().isoformat(),
            'country': fake.country(),
            'device': random.choice(['mobile', 'desktop', 'tablet'])
        }
        
        # Send to Kafka
        producer.send('ecommerce-events', value=event)
        
        event_count += 1
        print(f"Sent event #{event_count}: {event['event_type']} - {event['product']} - ${event['price']}")
        
        # Wait 1 second before next event
        time.sleep(1)
        
except KeyboardInterrupt:
    print(f"\nStopped! Total events sent: {event_count}")
    producer.close()