from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import List
import models
from pydantic import BaseModel

router = APIRouter()

class ClusteringResultBase(BaseModel):
    algorithm_id: int
    cluster: int
    count: int
    percentage: float
    midwest: int
    north: int
    northeast: int
    south: int
    southeast: int

class ClusteringResultCreate(ClusteringResultBase):
    pass

class ClusteringResult(ClusteringResultBase):
    id: int

    class Config:
        from_attributes = True

@router.get("/clustering-results", response_model=List[ClusteringResult])
def getAll_clustering_results(
    skip: int = 0,
    db: Session = Depends(get_db)
):
    clustering_results = db.query(models.ClusteringResults).offset(skip).all()
    return clustering_results 