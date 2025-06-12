from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import List
import models
from pydantic import BaseModel

router = APIRouter()

class ParameterBase(BaseModel):
    algorithm_id: int
    name: str
    value: str

class ParameterCreate(ParameterBase):
    pass

class Parameter(ParameterBase):
    id: int

    class Config:
        from_attributes = True

@router.get("/clustering/parameters/{algorithm_id}", response_model=List[Parameter])
def get_parameters(
    algorithm_id: int,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(models.Parameters).filter(models.Parameters.algorithm_id == algorithm_id)
    parameters = query.offset(skip).all()
    return parameters
