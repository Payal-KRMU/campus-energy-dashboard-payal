## 📋 Project Overview
An end-to-end energy consumption analysis and visualization system for campus buildings.

## 🎯 Learning Objectives
- Read and validate multiple datasets using Pandas
- Design object-oriented models for real-world systems
- Perform time-series and categorical aggregations
- Create effective multi-chart visualizations
- Automate data export and report generation

## 📁 Project Structure
campus-energy-dashboard-payal/
├── dashboard.py # Main Python script
├── data/ # Sample CSV data
│ ├── building1_jan.csv
│ └── building2_jan.csv
├── output/ # Generated outputs
│ ├── dashboard.png # Visualization dashboard
│ ├── cleaned_energy_data.csv
│ ├── building_summary.csv
│ └── summary.txt
└── README.md # This file

text

## 🛠️ Installation & Usage
1. Install dependencies
pip install pandas matplotlib

2. Generate sample data (if needed)
python create_csv.py

3. Run the dashboard
python dashboard.py

📊 Sample Insights
Total Campus Consumption: 2995.00 kWh
Highest Consuming Building: building2
Peak Load Time: 2024-01-04 00:00:00

Weekly Trends: Visible in dashboard visualization

📈 Key Features
* Automated data ingestion from multiple CSV files
* Object-oriented modeling (Building, MeterReading classes)
* Time-series analysis (daily/weekly aggregates)
* Professional 4-chart visualization dashboard
* Automated CSV export and text report generation
