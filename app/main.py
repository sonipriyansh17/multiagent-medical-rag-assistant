from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

# Import your services, models, and new DB setup
from app.services.rag_service import RAGService
from app.database import engine, Base, get_db
from app.models import Diagnosis # Import the new Diagnosis model

from fastapi.middleware.cors import CORSMiddleware
import os

from dotenv import load_dotenv 
load_dotenv()

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- Server starting up ---")
    # Create database tables on startup
    # This will create the 'diagnoses' table if it doesn't exist
    Base.metadata.create_all(bind=engine)
    print("--- Database tables checked/created. ---")
    
    ml_models["rag_service"] = RAGService()
    print("--- RAG Service Loaded. Server is ready. ---")
    yield
    print("--- Server shutting down ---")
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:3001"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiagnoseRequest(BaseModel):
    symptoms: str

@app.get("/")
def read_root():
    return {"status": "MedAssist API is running"}

# In backend/app/main.py

@app.post("/api/v1/diagnose")
async def diagnose(request: DiagnoseRequest, db: Session = Depends(get_db)):
    rag_service = ml_models.get("rag_service")
    if not rag_service or not rag_service.groq_client:
        raise HTTPException(status_code=503, detail="AI Service is not available. Check API key.")
    
    if not request.symptoms:
        raise HTTPException(status_code=400, detail="Symptoms cannot be empty.")

    try:
        # Step 1 & 2: Get the diagnosis from the RAG service
        retrieved_context = rag_service.retrieve_context(query=request.symptoms, top_k=5)
        generated_response = rag_service.generate_response(query=request.symptoms, context=retrieved_context)
        
        # ✨ STEP 3: Save the interaction to the database
        db_diagnosis = Diagnosis(
            symptoms=request.symptoms,
            diagnosis_response=generated_response
        )
        db.add(db_diagnosis)
        db.commit()
        db.refresh(db_diagnosis)
        
        print(f"\n--- Diagnosis saved to DB with ID: {db_diagnosis.id} ---")
        
        return {"diagnosis": generated_response}
        
    except Exception as e:
        print(f"An error occurred during diagnosis: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")

