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

@router.get("/clustering/metric-results/{algorithm_id}", response_model=List[MetricResult])
def get_metric_results(
    skip: int = 0,
    algorithm_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.MetricResults).filter(models.MetricResults.algorithm_id == algorithm_id)
    metrics_results = query.offset(skip).all()
    return metrics_results
