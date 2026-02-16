import pandas as pd
import os
from datetime import datetime

print("=" * 60)
print("DATA QUALITY CHECKS")
print("=" * 60)

# Read the latest raw events file
data_dir = '../data'
csv_files = [f for f in os.listdir(data_dir) if f.startswith('raw_events') and f.endswith('.csv')]
latest_file = sorted(csv_files)[-1]

print(f"\nAnalyzing: {latest_file}\n")

df = pd.read_csv(f"{data_dir}/{latest_file}")

# Quality Checks
issues_found = 0
total_checks = 0

print("Running Quality Checks...\n")

# Check 1: No null values
total_checks += 1
null_count = df.isnull().sum().sum()
if null_count == 0:
    print("✓ CHECK 1: No null values found")
else:
    print(f"✗ CHECK 1: Found {null_count} null values")
    print(f"  Columns with nulls: {df.isnull().sum()[df.isnull().sum() > 0].to_dict()}")
    issues_found += 1

# Check 2: Valid event types
total_checks += 1
valid_event_types = ['page_view', 'add_to_cart', 'purchase', 'search']
invalid_events = df[~df['event_type'].isin(valid_event_types)]
if len(invalid_events) == 0:
    print("✓ CHECK 2: All event types are valid")
else:
    print(f"✗ CHECK 2: Found {len(invalid_events)} invalid event types")
    print(f"  Invalid types: {invalid_events['event_type'].unique()}")
    issues_found += 1

# Check 3: Price range validation
total_checks += 1
min_price = 50
max_price = 2000
invalid_prices = df[(df['price'] < min_price) | (df['price'] > max_price)]
if len(invalid_prices) == 0:
    print(f"✓ CHECK 3: All prices within range (${min_price}-${max_price})")
else:
    print(f"✗ CHECK 3: Found {len(invalid_prices)} prices outside valid range")
    print(f"  Out of range prices: {invalid_prices['price'].tolist()}")
    issues_found += 1

# Check 4: Valid device types
total_checks += 1
valid_devices = ['mobile', 'desktop', 'tablet']
invalid_devices = df[~df['device'].isin(valid_devices)]
if len(invalid_devices) == 0:
    print("✓ CHECK 4: All device types are valid")
else:
    print(f"✗ CHECK 4: Found {len(invalid_devices)} invalid device types")
    print(f"  Invalid devices: {invalid_devices['device'].unique()}")
    issues_found += 1

# Check 5: No duplicate event IDs
total_checks += 1
duplicate_ids = df[df.duplicated(subset=['event_id'], keep=False)]
if len(duplicate_ids) == 0:
    print("✓ CHECK 5: No duplicate event IDs")
else:
    print(f"✗ CHECK 5: Found {len(duplicate_ids)} duplicate event IDs")
    issues_found += 1

# Check 6: Timestamp format validation
total_checks += 1
try:
    pd.to_datetime(df['timestamp'])
    print("✓ CHECK 6: All timestamps are valid")
except:
    print("✗ CHECK 6: Invalid timestamp format detected")
    issues_found += 1

# Check 7: Data completeness
total_checks += 1
expected_columns = ['event_id', 'event_type', 'user_id', 'product', 'price', 'timestamp', 'country', 'device']
missing_columns = [col for col in expected_columns if col not in df.columns]
if len(missing_columns) == 0:
    print("✓ CHECK 7: All expected columns present")
else:
    print(f"✗ CHECK 7: Missing columns: {missing_columns}")
    issues_found += 1

# Summary Statistics
print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)
print(f"Total Records: {len(df)}")
print(f"Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"Unique Users: {df['user_id'].nunique()}")
print(f"Unique Products: {df['product'].nunique()}")
print(f"Total Revenue: ${df[df['event_type'] == 'purchase']['price'].sum():,.2f}")
print(f"Average Event Price: ${df['price'].mean():.2f}")

# Quality Score
print("\n" + "=" * 60)
print("QUALITY SCORE")
print("=" * 60)
quality_score = ((total_checks - issues_found) / total_checks) * 100
print(f"Checks Passed: {total_checks - issues_found}/{total_checks}")
print(f"Quality Score: {quality_score:.1f}%")

if quality_score == 100:
    print("Status: ✓ EXCELLENT - All checks passed!")
elif quality_score >= 80:
    print("Status: ⚠ GOOD - Minor issues detected")
else:
    print("Status: ✗ POOR - Multiple issues need attention")

print("=" * 60)

# Save quality report
report_file = f"{data_dir}/quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(report_file, 'w') as f:
    f.write(f"Data Quality Report\n")
    f.write(f"Generated: {datetime.now()}\n")
    f.write(f"File: {latest_file}\n")
    f.write(f"Quality Score: {quality_score:.1f}%\n")
    f.write(f"Issues Found: {issues_found}\n")

print(f"\n✓ Quality report saved: {report_file}")