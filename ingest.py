import os
import glob
import pandas as pd

# Paths
RAW_EXPORT_DIR = "data/raw_exports"
STAGING_CSV = "data/raw_data.csv"

def ingest():
    """
    Ingestion step (file-based):
    - Finds the most recent CSV in data/raw_exports/
    - Reads it into a DataFrame
    - Checks for missing values (data profiling)
    - Writes the cleaned DataFrame to data/raw_data.csv for downstream stages
    """
    # 1. List CSV files in the export directory
    pattern = os.path.join(RAW_EXPORT_DIR, "*.csv")
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No CSV files found in {RAW_EXPORT_DIR}")
    
    # 2. Select the latest file by modification time
    latest_file = max(files, key=os.path.getmtime)
    print(f"Ingesting from latest file: {latest_file}")
    
    # 3. Load into DataFrame
    df = pd.read_csv(latest_file, parse_dates=["period_date"])
    
    # Check for missing values
    missing = df.isnull().sum()
    print("Missing values per column:\n", missing)
    
    # 4. Write to staging CSV
    df.to_csv(STAGING_CSV, index=False)
    print(f"Staged data written to {STAGING_CSV}")

if __name__ == "__main__":
    ingest()
