import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import torch
import os
from groq import Groq

# --- Configuration ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CHROMA_DB_PATH = BASE_DIR / "data" / "processed" / "embeddings"
MODEL_NAME = "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"
COLLECTION_NAME = "medical_knowledge_base"

class RAGService:
    def __init__(self):
        """
        Initializes the RAG Service by loading the model, ChromaDB, and the Groq client.
        """
        print("🔹 Initializing RAGService...")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(MODEL_NAME, device=self.device)
        self.client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
        self.collection = self.client.get_collection(name=COLLECTION_NAME)
        
        # Initialize Groq client
        try:
            self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            print("  - Groq client initialized.")
        except Exception as e:
            print(f"❌ ERROR: Groq API key not found. Please set the GROQ_API_KEY environment variable. {e}")
            self.groq_client = None

        print("✅ RAGService initialized successfully.")

    def retrieve_context(self, query: str, top_k: int = 5):
        """
        Retrieves the top_k most relevant documents from ChromaDB.
        """
        print(f"  - Retrieving context for query: '{query}'")
        query_embedding = self.model.encode(query, convert_to_tensor=True, device=self.device)
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        return results['documents'][0]

    def generate_response(self, query: str, context: list[str]):
        """
        Generates a response using an LLM, based on the retrieved context.
        """
        if not self.groq_client:
            return "Error: LLM client is not configured. Please check the API key."

        print(f"  - Generating response for query: '{query}'")
        # Create a system prompt to guide the LLM
        system_prompt = """
You are MedAssist AI, an advanced AI medical assistant. Your persona is professional, knowledgeable, and empathetic. Your primary function is to analyze a user's symptoms based on a provided context of medical documents and suggest potential conditions.

**Your Core Directives:**
1.  **Analyze and Filter:** Internally analyze the user's symptoms and the retrieved documents. Your most critical task is to identify which of the provided documents are **directly relevant** to the user's specific symptoms. **Silently and internally disregard all irrelevant documents.**
2.  **Synthesize Relevant Information:** Base your response **only** on the documents you have determined to be relevant. Do not mention the filtering process or the irrelevant documents in your final output.
3.  **Adopt a Clinical Tone:** Formulate your response in a clear, concise, and professional tone, as a doctor would.
4.  **Strict Output Format:** The user-facing response **must** adhere to the following structure precisely. Do not add any introductory text or explanation of your thought process. Begin your response *immediately* with the specified header.

---
**Possible Conditions Based on Your Symptoms:**

Based on the information provided, here are some potential conditions that could be related to your symptoms:

- **[Name of the Most Likely Condition]:** A brief, clinical explanation of why this condition is a potential match, directly referencing the user's symptoms.
- **[Name of the Second Most Likely Condition]:** A brief, clinical explanation of why this condition is a potential match.
- (Continue for all relevant conditions)

**Important Disclaimer:**

This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. It is essential to consult with a qualified healthcare provider for an accurate diagnosis and personalized treatment plan.
---
"""
        
        # Combine the context into a single string
        context_str = "\n\n".join(context)
        
        # Create the user message
        user_message = (
            f"Here is the context retrieved based on the user's symptoms:\n---CONTEXT---\n{context_str}\n\n---END CONTEXT---\n\n"
            f"Based on this context, please analyze the following user query: '{query}'"
        )
        
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            model="llama-3.3-70b-versatile", # Using Llama 3 8B model
        )
        
        return chat_completion.choices[0].message.content

