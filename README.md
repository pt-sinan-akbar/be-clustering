
# Clustering API
A FastAPI-based REST API for customer clustering analysis using various clustering algorithms.  
This project was developed as part of our thesis on comparing different clustering techniques.

## Setup

**1. Create a virtual environment (Python 3.11)**
```bash
python -m venv venv
```

**2. Activate the virtual environment**
- On Windows (PowerShell):
```bash
.\venv\Scripts\Activate.ps1
```
- On Linux/macOS
```bash
source venv/bin/activate
```


**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure env file:**
   - Rename `.env_dummy` to `.env`
   - Update the values in `.env` with your PostgreSQL database credentials

## Database Schema

The API uses PostgreSQL with the following models:
- `Algorithms`: Stores clustering algorithm information
- `Parameters`: Stores algorithm parameters
- `MetricResults`: Stores clustering metric results
- `Customers`: Stores customer data with RFM values and cluster assignments
- `ClusteringResults`: Stores clustering results with regional distribution

## Available Endpoints

The API is built with FastAPI and provides endpoints for:
- Retrieving clustering results
- Accessing customer data
- Getting algorithm metrics

## Running the Application

Start the server using uvicorn:
```bash
uvicorn main:app --reload
```

The API documentation will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
├── main.py          # FastAPI application and endpoints
├── database.py      # Database connection and configuration
├── models.py        # SQLAlchemy models
└── requirements.txt # Project dependencies
```

## Docker Guide
```bash
git clone https://github.com/dta32/be-clustering.git
cp .env_dummy .env # Update .env with your PostgreSQL credentials
docker build -t clustering-api .
docker run --name clustering-api-container -v $(pwd)/.env:/app/.env -d -p 8080:8080 clustering-api
```