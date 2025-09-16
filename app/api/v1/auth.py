from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/login")
async def login(db: Session = Depends(get_db)):
    return {"message": "Login endpoint - to be implemented"}

@router.post("/register")
async def register(db: Session = Depends(get_db)):
    return {"message": "Register endpoint - to be implemented"}
