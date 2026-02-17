import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import pandas as pd

dataset_dir = 'datasets'
if not os.path.exists(dataset_dir):
    print("No datasets folder found.")
else:
    for filename in os.listdir(dataset_dir):
        if filename.endswith('.csv'):
            print(f"\n--- Application {filename} ---")
            try:
                df = pd.read_csv(os.path.join(dataset_dir, filename))
                print(f"Columns: {list(df.columns)}")
                
                # Identify label column
                label_col = next((c for c in df.columns if 'label' in c.lower() or 'type' in c.lower() or 'class' in c.lower()), None)
                if label_col:
                    print(f"Label Column: {label_col}")
                    print("Sample Class 0/Phishing?:")
                    print(df[df[label_col].astype(str).str.contains('0|phish', case=False, regex=True)].head(3)[[df.columns[0], label_col]])
                    print("Sample Class 1/Safe?:")
                    print(df[df[label_col].astype(str).str.contains('1|safe|legit', case=False, regex=True)].head(3)[[df.columns[0], label_col]])
            except Exception as e:
                print(f"Error reading {filename}: {e}")
