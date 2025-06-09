
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
import models
from pydantic import BaseModel

router = APIRouter()

# Non Nullable
class CustomerBase(BaseModel):
    recency: float
    frequency: float
    monetary: float
    state: str

class CustomerCreate(CustomerBase):
    pass

# Nullable
class Customer(CustomerBase):
    id: str
    dbscan_cluster: Optional[int] = None
    hierarchical_cluster: Optional[int] = None
    gmm_cluster: Optional[int] = None
    kmeans_cluster: Optional[int] = None
    kprototypes_cluster: Optional[int] = None

    class Config:
        from_attributes = True

@router.get("/clustering/customers", response_model=List[Customer])
def get_all_customers(
    skip: int = 0,
    db: Session = Depends(get_db)
):
    customer = db.query(models.Customers).offset(skip).all()
    return customer
