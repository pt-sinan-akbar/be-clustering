from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from typing_extensions import Annotated  # Use typing_extensions for Python 3.7
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import pickle
import db_seeder

app = FastAPI(title="Clustering API")

@app.on_event("startup")
async def startup_event():
    with SessionLocal() as db:
        db_seeder.seeder(db)