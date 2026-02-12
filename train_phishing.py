import os
import requests
import pandas as pd
import io
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
                df = pd.read_csv(filepath)
            elif filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(filepath)
            
            if df is not None:
                print(f"Loading {filename}...")
                
                # Simple heuristic to find URL and Label columns
                # Adjust these based on specific dataset formats if needed
                url_col = next((c for c in df.columns if 'url' in c.lower()), None)
                label_col = next((c for c in df.columns if 'label' in c.lower() or 'type' in c.lower() or 'class' in c.lower() or 'status' in c.lower()), None)
                
                if url_col and label_col:
                    df = df.rename(columns={url_col: 'url'})
                    
                    # Specific handling for known datasets
                    if 'phiusiil' in filename.lower() or 'legitphish' in filename.lower():
                        # In these datasets: 0 = Phishing, 1 = Legitimate
                        # We want: 1 = Phishing, 0 = Legitimate
                        print(f"  -> Inverting labels for {filename} (assuming 0=Phishing, 1=Legit)...")
                        df['label'] = df[label_col].apply(lambda x: 0 if str(x) == '1' or str(x).lower() == 'legitimate' else 1)
                    else:
                        # Default handling (1=Phishing, 'phishing'=Phishing)
                        # Helper to normalize label values
                        def normalize_label(val):
                            s = str(val).lower().strip()
                            if s in ['1', 'phishing', 'bad', 'malicious', 'unsafe']:
                                return 1
                            if s in ['0', 'legitimate', 'safe', 'good', 'benign']:
                                return 0
                            return 0 # Default to safe if unsure
                            
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

    # 2. Train Model
    # To save time for this demo, let's sample if dataset is huge.
    if len(final_df) > 5000:
        print("Dataset > 5000. Sampling 5000 for quick training (since user is waiting).")
        # Ensure balanced sample
        phish = final_df[final_df['label'] == 1]
        legit = final_df[final_df['label'] == 0]
        n = min(len(phish), len(legit), 2500)
        final_df = pd.concat([phish.sample(n), legit.sample(n)]).sample(frac=1).reset_index(drop=True)

    classifier = PhishingClassifier()
    classifier.train(final_df)
    
    print("Training Complete!")

if __name__ == "__main__":
    main()
