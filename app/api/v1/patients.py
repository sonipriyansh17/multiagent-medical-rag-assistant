from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/")
async def list_patients(db: Session = Depends(get_db)):
    return {"message": "List patients endpoint - to be implemented"}

@router.post("/")
async def create_patient(db: Session = Depends(get_db)):
    return {"message": "Create patient endpoint - to be implemented"}
