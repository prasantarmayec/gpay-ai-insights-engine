"""
Train the ML/NLP categorizer for GPay AI Insights Engine.

Usage:
    python app/train_categorizer.py data/labeled_transactions.csv model/categorizer.pkl
"""

import sys
import pandas as pd
import joblib
from categorizer import train_ml_categorizer

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python app/train_categorizer.py <labeled_csv> <output_model_path>")
        sys.exit(1)
    csv_path = sys.argv[1]
    model_path = sys.argv[2]

    df = pd.read_csv(csv_path)
    # Expect columns: description, category
    X = (df["merchant"].fillna("") + " " + df["raw"].fillna("")).tolist()
    y = df["category"].tolist()

    model = train_ml_categorizer(X, y)
    joblib.dump(model, model_path)
    print(f"Trained model saved to {model_path}")
