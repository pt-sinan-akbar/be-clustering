from fastapi import Depends
from pydantic import BaseModel
from typing import List
from typing_extensions import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import pickle

# initialize db
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def seeder(db: Session):
    try:
        algorithms = [
            {"name": "K-MEANS"},
            {"name": "K-PROTOTYPES"},
            {"name": "DBSCAN"},
            {"name": "HIERARCHICAL"},
            {"name": "GMM"},
        ]
        
        # Check if algorithms already exist
        existing_algos = db.query(models.Algorithms).count()
        if existing_algos == 0:
            for algo_data in algorithms:
                algo = models.Algorithms(name=algo_data["name"])
                db.add(algo)
            db.flush()  # Flush to get the IDs without committing
            print(f"Added {len(algorithms)} algorithms")

        # Get algorithm IDs for parameter seeding
        kmeans = db.query(models.Algorithms).filter_by(name="K-MEANS").first()
        kprototypes = db.query(models.Algorithms).filter_by(name="K-PROTOTYPES").first()
        dbscan = db.query(models.Algorithms).filter_by(name="DBSCAN").first()
        hierarchical = db.query(models.Algorithms).filter_by(name="HIERARCHICAL").first()
        gmm = db.query(models.Algorithms).filter_by(name="GMM").first()

        parameters = [
            # K-MEANS parameters
            {"algorithm_id": kmeans.id, "name": "n_clusters", "value": "4"},
            {"algorithm_id": kmeans.id, "name": "random_state", "value": "42"},

            # K-PROTOTYPES parameters
            {"algorithm_id": kprototypes.id, "name": "n_clusters", "value": "5"},
            {"algorithm_id": kprototypes.id, "name": "random_state", "value": "42"},
            {"algorithm_id": kprototypes.id, "name": "init", "value": "huang"},
            {"algorithm_id": kprototypes.id, "name": "gamma", "value": "1.0"},

            # DBSCAN parameters
            {"algorithm_id": dbscan.id, "name": "eps", "value": "0.167682"},
            {"algorithm_id": dbscan.id, "name": "min_samples", "value": "13"},
            {"algorithm_id": dbscan.id, "name": "metric", "value": "euclidean"},

            # HIERARCHICAL parameters
            {"algorithm_id": hierarchical.id, "name": "n_clusters", "value": "4"},
            {"algorithm_id": hierarchical.id, "name": "linkage", "value": "ward"},

            # GMM parameters
            {"algorithm_id": gmm.id, "name": "n_components", "value": "3"},
            {"algorithm_id": gmm.id, "name": "random_state", "value": "42"}, 
        ]

        # Check if parameters already exist
        existing_params = db.query(models.Parameters).count()
        if existing_params == 0:
            for param_data in parameters:
                param = models.Parameters(
                    algorithm_id=param_data["algorithm_id"],
                    name=param_data["name"],
                    value=param_data["value"]
                )
                db.add(param)
            print(f"Added {len(parameters)} parameters")

        db.commit()
        print("Seeding completed successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise

if __name__ == "__main__":
    with SessionLocal() as db:
        seeder(db)