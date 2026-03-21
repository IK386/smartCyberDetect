import pandas as pd
import random
from datetime import datetime, timedelta

# ===========================
# Define columns
# ===========================
columns = ["timestamp","source_ip","dest_ip","protocol","packet_size","status"]

# ===========================
# Protocols and status options
# ===========================
protocols = ["TCP","UDP","ICMP"]
statuses = ["normal","suspicious","attack"]

# ===========================
# Generate 500 random records
# ===========================
records = []
start_time = datetime(2026,3,12,10,0,0)

for i in range(500):
    timestamp = start_time + timedelta(seconds=i*60)  # New record every minute
    source_ip = f"192.168.1.{random.randint(1,20)}"
    dest_ip = f"10.0.0.{random.randint(1,20)}"
    protocol = random.choice(protocols)
    packet_size = random.randint(50,2000)
    status = random.choices(statuses, weights=[60,20,20])[0]  # 60% normal, 20% suspicious, 20% attack
    records.append([timestamp.strftime("%Y-%m-%d %H:%M:%S"), source_ip, dest_ip, protocol, packet_size, status])

# ===========================
# Create DataFrame and save to CSV
# ===========================
df = pd.DataFrame(records, columns=columns)
df.to_csv("logs.txt", index=False)
print("✅ logs.txt generated with 500 records!")
print("✅ logs.txt generated with 500 records!")
print("✅ logs.txt generated with 500 records!")