import os

# Create data directory if not exists
os.makedirs('data', exist_ok=True)

# Building 1 data
building1_data = """timestamp,kwh
2024-01-01 00:00:00,150
2024-01-01 01:00:00,145
2024-01-02 00:00:00,160
2024-01-02 01:00:00,155
2024-01-03 00:00:00,170
2024-01-03 01:00:00,165
2024-01-04 00:00:00,180
2024-01-04 01:00:00,175"""

# Building 2 data
building2_data = """timestamp,kwh
2024-01-01 00:00:00,200
2024-01-01 01:00:00,190
2024-01-02 00:00:00,210
2024-01-02 01:00:00,205
2024-01-03 00:00:00,220
2024-01-03 01:00:00,215
2024-01-04 00:00:00,230
2024-01-04 01:00:00,225"""

# Write to files
with open('data/building1_jan.csv', 'w') as f:
    f.write(building1_data)

with open('data/building2_jan.csv', 'w') as f:
    f.write(building2_data)

print("✅ CSV files created successfully in data/ folder!")
print("Files created:")
print("1. data/building1_jan.csv")
print("2. data/building2_jan.csv")