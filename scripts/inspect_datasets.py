import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import pandas as pd
import traceback

dataset_dir = 'datasets'

def inspect_file(filepath):
    print(f"--- Inspecting {os.path.basename(filepath)} ---")
    try:
        if filepath.endswith('.csv'):
            try:
                # Try default encoding
                df = pd.read_csv(filepath, nrows=5)
            except UnicodeDecodeError:
                print("  -> UnicodeDecodeError with utf-8, trying latin1")
                df = pd.read_csv(filepath, nrows=5, encoding='latin1')
            except pd.errors.ParserError:
                 print("  -> ParserError, trying with error_bad_lines=False")
                 df = pd.read_csv(filepath, nrows=5, on_bad_lines='skip')

        elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            try:
                df = pd.read_excel(filepath, nrows=5)
            except ImportError as e:
                print(f"  -> Skipping Excel file due to missing dependency: {e}")
                return
        else:
            print("Skipping non-dataset file.")
            return

        if df is None or df.empty:
            print("  -> DataFrame is empty or None.")
        else:
            print("  -> Columns:", list(df.columns))
            print("  -> First 2 rows:")
            print(df.head(2))
            
            # Check for label distribution if label column exists
            possible_labels = [c for c in df.columns if 'label' in c.lower() or 'type' in c.lower()]
            if possible_labels:
                print(f"  -> Possible label columns: {possible_labels}")

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        # traceback.print_exc()
    print("--- End Inspection ---\n")

if os.path.exists(dataset_dir):
    files = sorted(os.listdir(dataset_dir))
    for filename in files:
        inspect_file(os.path.join(dataset_dir, filename))
else:
    print(f"Directory {dataset_dir} not found.")
