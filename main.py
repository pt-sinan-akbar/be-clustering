from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from typing_extensions import Annotated  # Use typing_extensions for Python 3.7
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import pickle

app = FastAPI(title="Clustering API")
# initialize db
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]