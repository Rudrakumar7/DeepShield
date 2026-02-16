import os
import requests
import pandas as pd
import io
import numpy as np
from utils.phishing_model import PhishingClassifier

def fetch_hf_dataset():
    """
    Fetches the 'ealvaradob/phishing-dataset' from HuggingFace (raw CSV).
    This dataset has 'url' and 'status' columns (phishing/legitimate).
    """
    print("Fetching HuggingFace dataset (ealvaradob/phishing-dataset)...")
    url = "https://huggingface.co/datasets/ealvaradob/phishing-dataset/resolve/main/phishing_dataset.csv"
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        
        # Standardize columns: 'url', 'label'
        # HF Status: 'phishing' or 'legitimate'
        df['label'] = df['status'].apply(lambda x: 1 if x == 'phishing' else 0)
        df = df[['url', 'label']]
        
        print(f"HF Dataset loaded: {len(df)} rows.")
        return df
    except Exception as e:
        print(f"Error fetching HF dataset: {e}")
        return pd.DataFrame()

def load_local_datasets():
    """
    Loads any CSV files found in 'datasets/' folder.
    Expects columns like 'url' and 'type'/'label'.
    """
    dataset_dir = 'datasets'
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        print(f"Created '{dataset_dir}' folder. Drop your CSVs here (LegitPhish, PhiUSIIL, etc.)!")
        return pd.DataFrame()

    all_dfs = []
    print(f"Checking '{dataset_dir}' for local datasets...")
    
    for filename in os.listdir(dataset_dir):
        filepath = os.path.join(dataset_dir, filename)
        try:
            df = None
            if filename.endswith('.csv'):
                # Handle potential parsing errors
                try:
                    df = pd.read_csv(filepath)
                except:
                    try:
                         df = pd.read_csv(filepath, encoding='latin1')
                    except:
                        print(f"  -> Could not read {filename} with utf-8 or latin1. Skipping.")
                        continue

            elif filename.endswith('.xlsx') or filename.endswith('.xls'):
                try:
                    df = pd.read_excel(filepath)
                except Exception as e:
                    print(f"  -> Skipping Excel file {filename}: {e}")
                    continue
            
            if df is not None:
                print(f"Loading {filename}...")
                
                # Normalize column names to lower case for easier matching
                df.columns = [c.strip() for c in df.columns]
                
                # Identify URL column
                url_col = next((c for c in df.columns if 'url' in c.lower()), None)
                
                # Identify Label column
                # Common names: label, type, class, status, ClassLabel
                label_col = next((c for c in df.columns if any(x in c.lower() for x in ['label', 'type', 'class', 'status'])), None)
                
                if url_col and label_col:
                    df = df.rename(columns={url_col: 'url'})
                    
                    # --- Specific Dataset Handling ---
                    
                    # 1. PhiUSIIL & url_features_extracted1.csv & MyDataSET.xlsx
                    # Findings: 
                    # - PhiUSIIL: 1=Legit (StackOverflow), 0=Phishing (Suspicious Google Docs).
                    # - Features: Same.
                    # - MyDataSET: 1=Legit (Wikipedia), 0=Phishing.
                    # We want: 1=Phishing, 0=Legit.
                    # So we must INVERT: 1 -> 0, 0 -> 1.
                    if 'phiusiil' in filename.lower() or 'features' in filename.lower() or 'mydataset' in filename.lower():
                        print(f"  -> Processing {filename} (INVERTING: 1=Legit->0, 0=Phish->1)...")
                        # Ensure numeric
                        df['label'] = pd.to_numeric(df[label_col], errors='coerce').fillna(0).astype(int)
                        # Invert
                        df['label'] = df['label'].apply(lambda x: 0 if x == 1 else 1)

                    # 2. Phishing URLs.csv
                    # Analysis: "Phishing" -> 1, "Legitimate" -> 0. (Correct as is)
                    elif 'phishing urls.csv' in filename.lower():
                         print(f"  -> Processing {filename} (Phishing=1, Legitimate=0)...")
                         df['label'] = df[label_col].apply(lambda x: 1 if str(x).strip().lower() == 'phishing' else 0)

                    # 3. URL dataset.csv
                    # Analysis: "phishing" -> 1, "legitimate" -> 0. (Correct as is)
                    elif 'url dataset.csv' in filename.lower():
                        print(f"  -> Processing {filename} (legitimate=0, phishing=1)...")
                        df['label'] = df[label_col].apply(lambda x: 1 if str(x).strip().lower() == 'phishing' else 0)

                    # 4. Default Heuristic
                    else:
                        print(f"  -> Processing {filename} with generic heuristic...")
                        def normalize_label(val):
                            s = str(val).lower().strip()
                            if s in ['1', 'phishing', 'bad', 'malicious', 'unsafe']:
                                return 1
                            if s in ['0', 'legitimate', 'safe', 'good', 'benign']:
                                return 0
                             # Some datasets use -1 for phishing or legit.
                            if s == '-1': 
                                return 1 # Assumption
                            return 0 
                            
                        df['label'] = df[label_col].apply(normalize_label)
                    
                    df = df[['url', 'label']]
                    all_dfs.append(df)
                    print(f"  -> Added {len(df)} rows from {filename}")
                else:
                    print(f"  -> Skipped {filename}: Could not identify 'url' and 'label' columns. Found: {list(df.columns)}")
        except Exception as e:
            print(f"Error reading {filename}: {e}")
                
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return pd.DataFrame()

def main():
    # 1. Gather Data
    hf_data = fetch_hf_dataset()
    local_data = load_local_datasets()
    
    final_df = pd.concat([hf_data, local_data], ignore_index=True)
    
    if final_df.empty:
        print("No training data found! Please add datasets to 'datasets/' folder or check internet connection.")
        return

    # Remove duplicates
    original_len = len(final_df)
    final_df.drop_duplicates(subset=['url'], inplace=True)
    print(f"Training on {len(final_df)} unique URLs (removed {original_len - len(final_df)} duplicates).")
    
    print(f"Phishing samples: {len(final_df[final_df['label'] == 1])}")
    print(f"Legit samples: {len(final_df[final_df['label'] == 0])}")

    # DEBUG: Check labels for known safe sites
    print("\n--- DEBUG: Label Check ---")
    safe_sites = ['google.com', 'youtube.com', 'wikipedia.org', 'amazon.com', 'stackoverflow.com']
    for site in safe_sites:
        matches = final_df[final_df['url'].str.contains(site, case=False, na=False)]
        if not matches.empty:
            print(f"Samples for {site}:")
            print(matches[['url', 'label']].head(5))
            print(f"  -> Avg Label (should be near 0): {matches['label'].mean():.2f}")
    print("--------------------------\n")

    # 2. Train Model
    # Removed 5000 row limit. Training on full dataset.
    print("Starting training on full dataset...")
    
    # Optional: If dataset is MASSIVE (>500k), maybe warn or sample. 
    # But user asked to train on provided datasets, so we use all.

    classifier = PhishingClassifier()
    classifier.train(final_df)
    
    print("Training Complete!")

if __name__ == "__main__":
    main()
