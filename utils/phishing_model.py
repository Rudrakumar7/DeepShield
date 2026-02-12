import re
import os
import pickle
import numpy as np
import pandas as pd
from urllib.parse import urlparse
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class PhishingClassifier:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), 'phishing_model.pkl')

    def extract_features(self, url):
        """
        Extracts numerical features from a URL for the ML model.
        Returns a list of feature values.
        """
        parsed = urlparse(url)
        hostname = parsed.netloc
        path = parsed.path
        
        features = []
        
        # 1. Length Features
        features.append(len(url))
        features.append(len(hostname))
        features.append(len(path))
        
        # 2. Count Features
        features.append(url.count('.'))
        features.append(url.count('-'))
        features.append(url.count('@'))
        features.append(url.count('?'))
        features.append(url.count('&'))
        features.append(url.count('='))
        features.append(url.count('_'))
        features.append(url.count('~'))
        features.append(url.count('%'))
        features.append(url.count('/'))
        
        # 3. Binary Features
        features.append(1 if parsed.scheme == 'https' else 0)
        
        # IP Address check
        ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        features.append(1 if re.search(ip_pattern, hostname) else 0)
        
        # Shortening service check (simple list)
        shorteners = ['bit.ly', 'goo.gl', 'shorte.st', 'go2l.ink', 'x.co', 'ow.ly', 't.co', 'tinyurl', 'tr.im', 'is.gd', 'cli.gs']
        features.append(1 if any(s in hostname for s in shorteners) else 0)
        
        # 4. Digit Count
        features.append(sum(c.isdigit() for c in url))
        features.append(sum(c.isdigit() for c in hostname))
        
        return features

    def train(self, df):
        """
        Trains the XGBoost model on the provided DataFrame.
        df must have 'url' and 'label' columns (0=legit, 1=phishing).
        """
        print("Extracting features for training data...")
        X = []
        y = df['label'].values
        
        for url in df['url']:
            X.append(self.extract_features(url))
            
        X = np.array(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = XGBClassifier(
            max_depth=5, 
            learning_rate=0.1, 
            n_estimators=100, 
            use_label_encoder=False, 
            eval_metric='logloss'
        )
        
        print("Training XGBoost model...")
        self.model.fit(X_train, y_train)
        
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model trained. Accuracy: {accuracy:.4f}")
        print(classification_report(y_test, predictions))
        
        self.save_model()
        return accuracy

    def predict(self, url):
        """
        Predicts if a URL is phishing.
        Returns: properbility (0.0 to 1.0) where 1.0 is phishing.
        """
        if not self.model:
            if not self.load_model():
                return None # Model not ready
                
        features = np.array([self.extract_features(url)])
        prob_phishing = self.model.predict_proba(features)[0][1]
        return prob_phishing

    def save_model(self):
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {self.model_path}")

    def load_model(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            return True
        return False
