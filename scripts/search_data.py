import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import pandas as pd

dataset_dir = 'datasets'
term = 'github.com'

print(f"Searching for '{term}' in datasets...")

for filename in os.listdir(dataset_dir):
    if filename.endswith('.csv'):
        try:
            df = pd.read_csv(os.path.join(dataset_dir, filename))
            # specialized reading similar to training script to get correct 'label'
            url_col = next((c for c in df.columns if 'url' in c.lower()), None)
            label_col = next((c for c in df.columns if 'label' in c.lower() or 'type' in c.lower() or 'class' in c.lower()), None)
            
            if url_col and label_col:
                matches = df[df[url_col].astype(str).str.contains(term, case=False, regex=False)]
                if not matches.empty:
                    print(f"\n--- {filename} ---")
                    print(f"Found {len(matches)} matches.")
                    print(matches[[url_col, label_col]].head(10))
        except Exception as e:
            pass
