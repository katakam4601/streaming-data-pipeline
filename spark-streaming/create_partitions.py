import pandas as pd
from datetime import datetime
import os

print("=" * 50)
print("Creating Partitioned Data Structure (S3 Style)")
print("=" * 50)

# Read the latest parquet file
data_dir = '../data'
parquet_files = [f for f in os.listdir(data_dir) if f.startswith('raw_events') and f.endswith('.parquet')]
latest_file = sorted(parquet_files)[-1]

print(f"\nReading: {latest_file}")
df = pd.read_parquet(f"{data_dir}/{latest_file}")

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['year'] = df['timestamp'].dt.year
df['month'] = df['timestamp'].dt.month
df['day'] = df['timestamp'].dt.day
df['hour'] = df['timestamp'].dt.hour

print(f"Total events: {len(df)}")

# Create partitioned structure
partition_base = '../data/partitioned'
os.makedirs(partition_base, exist_ok=True)

print("\nCreating partitions...")

# Group by year/month/day/hour and save
partitions_created = 0
for (year, month, day, hour), group in df.groupby(['year', 'month', 'day', 'hour']):
    # Create directory structure: year=2024/month=02/day=16/hour=01/
    partition_path = f"{partition_base}/year={year}/month={month:02d}/day={day:02d}/hour={hour:02d}"
    os.makedirs(partition_path, exist_ok=True)
    
    # Save as parquet
    output_file = f"{partition_path}/data.parquet"
    group.drop(['year', 'month', 'day', 'hour'], axis=1).to_parquet(output_file, index=False)
    
    partitions_created += 1
    print(f"  ✓ {partition_path} ({len(group)} events)")

print(f"\n{'=' * 50}")
print(f"Partitioning Complete!")
print(f"Created {partitions_created} partitions")
print(f"Location: {partition_base}")
print(f"{'=' * 50}")

# Show directory structure
print("\nDirectory Structure:")
for root, dirs, files in os.walk(partition_base):
    level = root.replace(partition_base, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    sub_indent = ' ' * 2 * (level + 1)
    for file in files:
        print(f"{sub_indent}{file}")