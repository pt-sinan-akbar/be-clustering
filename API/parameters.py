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

@router.get("/parameters", response_model=List[Parameter])
def getAll_parameters(
    skip: int = 0,
    db: Session = Depends(get_db)
):
    parameters = db.query(models.Parameters).offset(skip).all()
    return parameters 