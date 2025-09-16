import pandas as pd
from pathlib import Path

# Get backend root
BASEDIR = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = BASEDIR.parent / "data" / "raw" / "disease_symptom.csv"
PROCESSED_DATA_PATH = BASEDIR.parent / "data" / "processed" / "medical_dataset_clean.csv"

def clean_dataset(df):
    df = df.drop_duplicates()
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)  # applymap deprecated
    df = df.dropna()
    return df

if __name__ == "__main__":
    print("Backend dir:", BASEDIR)
    print("Looking for dataset at:", RAW_DATA_PATH)

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    print(f"Raw dataset shape: {df.shape}")

    df_clean = clean_dataset(df)
    print(f"Clean dataset shape: {df_clean.shape}")

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"✅ Cleaned dataset saved at {PROCESSED_DATA_PATH}")
