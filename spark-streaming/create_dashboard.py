import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

print("=" * 50)
print("Creating Visualization Dashboard")
print("=" * 50)

# Read the latest CSV files
data_dir = '../data'

# Find latest files
csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
product_file = [f for f in csv_files if 'product_metrics' in f][-1]
raw_file = [f for f in csv_files if 'raw_events' in f][-1]

print(f"\nReading data files...")
print(f"  - {product_file}")
print(f"  - {raw_file}")

# Load data
df_products = pd.read_csv(f"{data_dir}/{product_file}")
df_raw = pd.read_csv(f"{data_dir}/{raw_file}")

# Calculate event counts from raw data
df_events = df_raw['event_type'].value_counts().reset_index()
df_events.columns = ['event_type', 'count']

# Create figure with 4 subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('E-Commerce Analytics Dashboard', fontsize=16, fontweight='bold')

# 1. Event Type Distribution (Pie Chart)
ax1.pie(df_events['count'], labels=df_events['event_type'], autopct='%1.1f%%', startangle=90)
ax1.set_title('Event Type Distribution')

# 2. Product Revenue (Bar Chart)
df_products_sorted = df_products.sort_values('total_revenue', ascending=False)
ax2.bar(df_products_sorted['product'], df_products_sorted['total_revenue'], color='skyblue')
ax2.set_title('Total Revenue by Product')
ax2.set_xlabel('Product')
ax2.set_ylabel('Revenue ($)')
ax2.tick_params(axis='x', rotation=45)

# 3. Average Price by Product (Horizontal Bar)
df_products_sorted_price = df_products.sort_values('avg_price', ascending=True)
ax3.barh(df_products_sorted_price['product'], df_products_sorted_price['avg_price'], color='lightcoral')
ax3.set_title('Average Price by Product')
ax3.set_xlabel('Price ($)')
ax3.set_ylabel('Product')

# 4. Device Distribution (Bar Chart)
device_counts = df_raw['device'].value_counts()
ax4.bar(device_counts.index, device_counts.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax4.set_title('Events by Device Type')
ax4.set_xlabel('Device')
ax4.set_ylabel('Number of Events')

# Adjust layout
plt.tight_layout()

# Save dashboard
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
dashboard_file = f"{data_dir}/dashboard_{timestamp}.png"
plt.savefig(dashboard_file, dpi=300, bbox_inches='tight')

print(f"\n✓ Dashboard created: {dashboard_file}")

# Display dashboard
plt.show()

print("\n" + "=" * 50)
print("Dashboard Complete!")
print("=" * 50)