# Setup Guide

## Step-by-Step Installation

### 1. Install Docker Desktop
- Download from: https://www.docker.com/products/docker-desktop
- Install and start Docker
- Verify: `docker --version`

### 2. Install Python 3.8+
- Download from: https://www.python.org/downloads/
- Verify: `python --version`

### 3. Clone Project
```bash
git clone <your-repo-url>
cd streaming-data-pipeline
```

### 4. Install Dependencies
```bash
pip install kafka-python faker pandas pyarrow matplotlib
```

### 5. Start Kafka
```bash
docker-compose up -d
```

Verify Kafka is running:
```bash
docker ps
```

You should see 2 containers running (Kafka and Zookeeper)

### 6. Run the Pipeline

**Terminal 1 - Start Producer:**
```bash
cd kafka-producer
python producer.py
# Let it run for 30-60 seconds
# Press Ctrl+C to stop
```

**Terminal 2 - Process Data:**
```bash
cd spark-streaming
python batch_processor.py
python create_partitions.py
python create_dashboard.py
python data_quality_checks.py
```

## Troubleshooting

### Docker not starting
- Make sure Docker Desktop is running
- Try: `docker-compose down` then `docker-compose up -d`

### Kafka connection refused
- Wait 30 seconds after starting Docker for Kafka to initialize
- Check: `docker logs streaming-data-pipeline-kafka-1`

### Python package errors
- Upgrade pip: `pip install --upgrade pip`
- Reinstall packages: `pip install --force-reinstall <package-name>`

## Stopping Everything
```bash
# Stop Kafka
docker-compose down

# Stop producer (if running)
Ctrl+C
```

## File Locations

- Raw events: `data/raw_events_*.csv` and `*.parquet`
- Processed metrics: `data/product_metrics_*.csv`
- Partitioned data: `data/partitioned/year=*/month=*/day=*/hour=*/`
- Dashboards: `data/dashboard_*.png`
- Quality reports: `data/quality_report_*.txt`