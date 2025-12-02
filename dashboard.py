import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---------------------------
# Task 1: Data Ingestion
# ---------------------------
def load_and_combine_data(data_dir='data'):
    dfs = []
    data_path = Path(data_dir)
    
    if not data_path.exists():
        logging.error(f"Directory {data_dir} not found.")
        return pd.DataFrame()
    
    for file in data_path.glob("*.csv"):
        try:
            df = pd.read_csv(file, on_bad_lines='skip')
            # Extract building name from filename
            building = file.stem.split('_')[0]
            df['building'] = building
            dfs.append(df)
            logging.info(f"Loaded {file}")
        except Exception as e:
            logging.warning(f"Failed to load {file}: {e}")
    
    if not dfs:
        logging.warning("No CSV files found.")
        return pd.DataFrame()
    
    combined = pd.concat(dfs, ignore_index=True)
    combined['timestamp'] = pd.to_datetime(combined['timestamp'], errors='coerce')
    combined.dropna(subset=['timestamp', 'kwh'], inplace=True)
    logging.info(f"Combined shape: {combined.shape}")
    return combined

# ---------------------------
# Task 2: Aggregation Functions
# ---------------------------
def calculate_daily_totals(df):
    df['date'] = df['timestamp'].dt.date
    daily = df.groupby(['date', 'building'])['kwh'].sum().reset_index()
    return daily

def calculate_weekly_aggregates(df):
    df['week'] = df['timestamp'].dt.to_period('W')
    weekly = df.groupby(['week', 'building'])['kwh'].sum().reset_index()
    return weekly

def building_wise_summary(df):
    summary = df.groupby('building')['kwh'].agg(['mean', 'min', 'max', 'sum']).reset_index()
    summary.columns = ['building', 'avg_kwh', 'min_kwh', 'max_kwh', 'total_kwh']
    return summary

# ---------------------------
# Task 3: OOP Modeling
# ---------------------------
class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []
    
    def add_reading(self, timestamp, kwh):
        self.readings.append(MeterReading(timestamp, kwh))
    
    def total_consumption(self):
        return sum(r.kwh for r in self.readings)
    
    def generate_report(self):
        total = self.total_consumption()
        return f"Building: {self.name}, Total Consumption: {total:.2f} kWh"

class BuildingManager:
    def __init__(self):
        self.buildings = {}
    
    def add_building(self, name):
        self.buildings[name] = Building(name)
    
    def add_reading_to_building(self, building_name, timestamp, kwh):
        if building_name not in self.buildings:
            self.add_building(building_name)
        self.buildings[building_name].add_reading(timestamp, kwh)

# ---------------------------
# Task 4: Visualization
# ---------------------------
def create_dashboard(df, daily_totals, weekly_agg, building_summary):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Campus Energy Dashboard", fontsize=16)
    
    # 1. Line plot: daily trend
    ax1 = axes[0, 0]
    for building in daily_totals['building'].unique():
        b_data = daily_totals[daily_totals['building'] == building]
        ax1.plot(b_data['date'], b_data['kwh'], marker='o', label=building)
    ax1.set_title("Daily Consumption Trend")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("kWh")
    ax1.legend()
    ax1.grid(True)
    
    # 2. Bar chart: weekly avg per building
    ax2 = axes[0, 1]
    weekly_avg = weekly_agg.groupby('building')['kwh'].mean()
    ax2.bar(weekly_avg.index, weekly_avg.values, color='skyblue')
    ax2.set_title("Average Weekly Consumption per Building")
    ax2.set_xlabel("Building")
    ax2.set_ylabel("Avg kWh")
    
    # 3. Scatter: peak vs time
    ax3 = axes[1, 0]
    df['hour'] = df['timestamp'].dt.hour
    peak_hours = df.groupby(['building', 'hour'])['kwh'].max().reset_index()
    for building in peak_hours['building'].unique():
        b_data = peak_hours[peak_hours['building'] == building]
        ax3.scatter(b_data['hour'], b_data['kwh'], label=building, alpha=0.7)
    ax3.set_title("Peak Hour Consumption")
    ax3.set_xlabel("Hour of Day")
    ax3.set_ylabel("Peak kWh")
    ax3.legend()
    
    # 4. Summary table
    ax4 = axes[1, 1]
    ax4.axis('off')
    table_data = building_summary.values
    col_labels = building_summary.columns
    ax4.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
    ax4.set_title("Building Summary")
    
    plt.tight_layout()
    plt.savefig('output/dashboard.png')
    logging.info("Dashboard saved as output/dashboard.png")

# ---------------------------
# Task 5: Export and Summary
# ---------------------------
def export_results(df, daily, weekly, summary):
    # Export cleaned data
    df.to_csv('output/cleaned_energy_data.csv', index=False)
    summary.to_csv('output/building_summary.csv', index=False)
    
    # Generate text summary
    total_consumption = df['kwh'].sum()
    highest_building = summary.loc[summary['total_kwh'].idxmax(), 'building']
    peak_time = df.loc[df['kwh'].idxmax(), 'timestamp']
    
    with open('output/summary.txt', 'w') as f:
        f.write("CAMPUS ENERGY CONSUMPTION REPORT\n")
        f.write("="*40 + "\n")
        f.write(f"Total Campus Consumption: {total_consumption:.2f} kWh\n")
        f.write(f"Highest Consuming Building: {highest_building}\n")
        f.write(f"Peak Load Time: {peak_time}\n")
        f.write(f"Number of Buildings: {len(summary)}\n")
        f.write(f"Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}\n")
    
    logging.info("Data exported to /output folder")

# ---------------------------
# Main Execution
# ---------------------------
if __name__ == "__main__":
    logging.info("Starting Campus Energy Dashboard Pipeline")
    
    # Task 1
    df = load_and_combine_data('data')
    if df.empty:
        logging.error("No data to process. Exiting.")
        exit(1)
    
    # Task 2
    daily = calculate_daily_totals(df)
    weekly = calculate_weekly_aggregates(df)
    summary = building_wise_summary(df)
    
    # Task 3: OOP example
    manager = BuildingManager()
    for _, row in df.iterrows():
        manager.add_reading_to_building(row['building'], row['timestamp'], row['kwh'])
    
    for name, building in manager.buildings.items():
        print(building.generate_report())
    
    # Task 4
    create_dashboard(df, daily, weekly, summary)
    
    # Task 5
    export_results(df, daily, weekly, summary)
    
    logging.info("Pipeline completed successfully!")