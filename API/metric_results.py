from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import List
import models
from pydantic import BaseModel

router = APIRouter()

class MetricResultBase(BaseModel):
    algorithm_id: int
    metric_name: str
    metric_value: float

class MetricResultCreate(MetricResultBase):
    pass

class MetricResult(MetricResultBase):
    id: int

    class Config:
        from_attributes = True

@router.get("/metric-results", response_model=List[MetricResult])
def getAll_metric_results(
    skip: int = 0,
    db: Session = Depends(get_db)
):
    metric_results = db.query(models.MetricResults).offset(skip).all()
    return metric_results 