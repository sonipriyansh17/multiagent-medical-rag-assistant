import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
import torch
import sys


try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
    print("🔹 Using pysqlite3-binary for SQLite.")
except ImportError:
    print("🔹 pysqlite3-binary not found. Using system's default SQLite.")
    pass

# --- GPU Acceleration Setup ---
# Check if a CUDA-enabled GPU is available and set the device accordingly.
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"🔹 Using device: {device}")
if device == 'cuda':
    print(f"🔹 GPU Device: {torch.cuda.get_device_name(0)}")

# --- Dynamic Path Configuration ---
# Build paths relative to the script's location to ensure it works anywhere.
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DATA_PATH = BASE_DIR.parent / "data" / "processed" / "medical_dataset_clean.csv"
CHROMA_DB_PATH = BASE_DIR.parent / "data" / "processed" / "embeddings"
print(f"🔹 Cleaned data path: {CLEAN_DATA_PATH}")
print(f"🔹 ChromaDB storage path: {CHROMA_DB_PATH}")

# --- Main Embedding Generation Logic ---
def create_and_store_embeddings():
    """
    Loads cleaned medical data, generates embeddings using a GPU (if available),
    and stores them in a persistent ChromaDB collection.
    """
    # 1. Load the cleaned dataset
    try:
        df = pd.read_csv(CLEAN_DATA_PATH)
        print(f"✅ Successfully loaded cleaned dataset with shape: {df.shape}")
    except FileNotFoundError:
        print(f"❌ ERROR: Cleaned data file not found at {CLEAN_DATA_PATH}")
        print("Please run the 'load_medical_data.py' script first.")
        return

    # 2. Load the Sentence Transformer model
    # The model is explicitly moved to the selected device (GPU/CPU).
    MODEL_NAME = "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"
    print(f"🔹 Loading embedding model: {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME, device=device)
    print("✅ Model loaded successfully.")

    # 3. Connect to ChromaDB and create a collection
    client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
    collection = client.get_or_create_collection(name="medical_knowledge_base")
    print(f"✅ Connected to ChromaDB. Collection 'medical_knowledge_base' is ready.")

    # 4. Prepare data for embedding
    # We create descriptive sentences for each disease-symptom combination.
    texts = []
    metadatas = []
    ids = []

    print("🔹 Preparing data for embedding...")
    for idx, row in df.iterrows():
        disease = row[0]  # The first column is the disease name
        # Collect all symptoms for the current disease
        symptoms = ", ".join([col.replace('_', ' ') for col in df.columns[1:] if row[col] == 1])
        
        # Create a descriptive text string
        text = f"The patient has {disease}, with symptoms including: {symptoms}."
        
        texts.append(text)
        ids.append(str(idx))
        metadatas.append({"disease": disease, "symptoms": symptoms})

    # 5. Generate embeddings in batches
    # Using a batch size helps manage memory, especially on GPUs with limited VRAM.
    print(f"🔹 Creating {len(texts)} embeddings... (This may take a while)")
    batch_size = 32 # Adjust based on your VRAM (e.g., 16, 32, 64)
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        batch_size=batch_size,
        device=device
    )
    print("✅ Embeddings generated.")

    # 6. Add embeddings to ChromaDB collection
    # We add the data in chunks to avoid overwhelming the database connection.
    print("🔹 Storing embeddings in ChromaDB...")
    total_items = len(ids)
    chunk_size = 1000 # Process 1000 items at a time

    for i in range(0, total_items, chunk_size):
        end_index = min(i + chunk_size, total_items)
        collection.add(
            ids=ids[i:end_index],
            documents=texts[i:end_index],
            embeddings=embeddings[i:end_index].tolist(), # Convert numpy array to list
            metadatas=metadatas[i:end_index],
        )
        print(f"  - Stored chunk {i//chunk_size + 1}/{(total_items + chunk_size - 1)//chunk_size}")

    print(f"🎉 Success! Stored {collection.count()} medical entries in ChromaDB.")
    print("Phase 2 is complete. You are ready to build the RAG pipeline.")

if __name__ == "__main__":
    create_and_store_embeddings()

