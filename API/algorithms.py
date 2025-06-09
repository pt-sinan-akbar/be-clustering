from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import List
import models
from pydantic import BaseModel

router = APIRouter()

class AlgorithmBase(BaseModel):
    name: str

class AlgorithmCreate(AlgorithmBase):
    pass

class Algorithm(AlgorithmBase):
    id: int

    class Config:
        from_attributes = True

@router.get("/clustering/algorithms", response_model=List[Algorithm])
def get_all_algorithms(
    skip: int = 0,
    db: Session = Depends(get_db)
):
    algorithms = db.query(models.Algorithms).offset(skip).all()
    return algorithms

