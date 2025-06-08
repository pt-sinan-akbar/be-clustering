from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from typing_extensions import Annotated  # Use typing_extensions for Python 3.7
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import pickle
import db_seeder
from API import customers, algorithms, parameters, metric_results, clustering_results

app = FastAPI(title="Clustering API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers.router, prefix="/api/v1", tags=["customers"])
app.include_router(algorithms.router, prefix="/api/v1", tags=["algorithms"])
app.include_router(parameters.router, prefix="/api/v1", tags=["parameters"])
app.include_router(metric_results.router, prefix="/api/v1", tags=["metric-results"])
app.include_router(clustering_results.router, prefix="/api/v1", tags=["clustering-results"])

@app.on_event("startup")
async def startup_event():
    with SessionLocal() as db:
        db_seeder.seeder(db)