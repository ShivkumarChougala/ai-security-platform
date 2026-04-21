from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db

router = APIRouter()

@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"message": "Database connected successfully"}
