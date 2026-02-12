import os
import pandas as pd
import traceback

dataset_dir = 'datasets'

def inspect_file(filepath):
    print(f"--- Inspecting {os.path.basename(filepath)} ---")
    try:
        if filepath.endswith('.csv'):
            try:
                df = pd.read_csv(filepath, nrows=5)
            except Exception:
                # Try with different encoding if default fails
                 df = pd.read_csv(filepath, nrows=5, encoding='latin1')
        elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            df = pd.read_excel(filepath, nrows=5)
        else:
            print("Skipping non-dataset file.")
            return

        if df.empty:
            print("DataFrame is empty.")
        else:
            print("Columns:", list(df.columns))
            print("First 2 rows:")
            print(df.head(2))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        traceback.print_exc()
    print("--- End Inspection ---\n")

if os.path.exists(dataset_dir):
    files = sorted(os.listdir(dataset_dir))
    for filename in files:
        inspect_file(os.path.join(dataset_dir, filename))
else:
    print(f"Directory {dataset_dir} not found.")
