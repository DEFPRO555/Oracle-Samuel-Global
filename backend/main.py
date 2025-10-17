# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL - FastAPI Backend Server
# Production-grade REST API for Oracle Samuel AI System

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn
from typing import Optional, List
import pandas as pd
import numpy as np
from datetime import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from pydantic import BaseModel, Field
from enum import Enum
import logging
from redis import Redis
from sqlalchemy.orm import Session

# Import Oracle Samuel modules
from utils.md5_manager import generate_md5_from_dataframe
from utils.database_manager import DatabaseManager
from utils.predictor import RealEstatePredictor
from self_learning.trainer import SelfLearningTrainer
from self_learning.evaluator import ModelEvaluator
from agent import OracleSamuelAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "request_id": "%(request_id)s"}',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Oracle Samuel API",
    description="AI-Powered Real Estate Analytics & Prediction Engine",
    version="5.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Security
security = HTTPBearer()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Redis connection for caching and task queue
redis_client = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

# Database
db_manager = DatabaseManager()

# Pydantic Models
class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class DatasetUploadRequest(BaseModel):
    dataset_name: str = Field(..., description="Name of the dataset")
    description: Optional[str] = Field(None, description="Dataset description")

class PredictionRequest(BaseModel):
    area: float = Field(..., gt=0, description="Property area in square meters")
    rooms: int = Field(..., ge=1, le=20, description="Number of rooms")
    bedrooms: int = Field(..., ge=0, le=15, description="Number of bedrooms")
    bathrooms: int = Field(..., ge=1, le=10, description="Number of bathrooms")
    parking_spots: int = Field(..., ge=0, le=10, description="Number of parking spots")
    floor: int = Field(..., ge=-2, le=100, description="Floor number")
    animal: bool = Field(default=False, description="Allows pets")
    furniture: bool = Field(default=False, description="Furnished")
    city: str = Field(..., description="City name")
    district: Optional[str] = Field(None, description="District/neighborhood")
    
class PredictionResponse(BaseModel):
    predicted_price: float
    confidence_interval: dict
    similar_properties: List[dict]
    market_insights: dict
    request_id: str

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    result: Optional[dict] = None
    error: Optional[str] = None

class ModelInfo(BaseModel):
    model_id: str
    version: str
    md5_hash: str
    metrics: dict
    created_at: datetime
    is_active: bool

class FeedbackRequest(BaseModel):
    prediction_id: str
    actual_price: float
    user_rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = None

# Dependency: Verify API Key
async def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token or API key"""
    token = credentials.credentials
    # TODO: Implement JWT validation
    # For now, check against environment variable
    if token != os.getenv("API_SECRET_KEY", "change_me"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return token

# Health Check Endpoints
@app.get("/health", tags=["System"])
async def health_check():
    """Liveness probe - service is running"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/ready", tags=["System"])
async def readiness_check():
    """Readiness probe - service can accept traffic"""
    try:
        # Check database
        db_manager.execute_query("SELECT 1")
        # Check Redis
        redis_client.ping()
        return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service not ready")

# Dataset Upload Endpoint
@app.post("/api/v1/upload", response_model=JobResponse, tags=["Data"])
async def upload_dataset(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    dataset_name: str = "",
    description: str = "",
    api_key: str = Depends(verify_api_key)
):
    """
    Upload a dataset for training Oracle Samuel.
    Returns a job ID for tracking processing status.
    """
    import uuid
    job_id = str(uuid.uuid4())
    
    try:
        # Read uploaded file
        contents = await file.read()
        
        # Determine file type and read
        if file.filename.endswith('.csv'):
            df = pd.read_csv(pd.io.common.BytesIO(contents))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(pd.io.common.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use CSV or Excel.")
        
        # Generate MD5
        md5_hash = generate_md5_from_dataframe(df)
        
        # Save to object store (S3/GCS)
        # TODO: Implement object store upload
        
        # Create job record
        job_data = {
            "job_id": job_id,
            "status": JobStatus.PENDING,
            "dataset_name": dataset_name or file.filename,
            "md5_hash": md5_hash,
            "row_count": len(df),
            "created_at": datetime.utcnow()
        }
        
        # Store job in Redis
        redis_client.setex(f"job:{job_id}", 3600, json.dumps(job_data, default=str))
        
        # Enqueue background task
        background_tasks.add_task(process_dataset, job_id, df, md5_hash)
        
        logger.info(f"Dataset uploaded successfully. Job ID: {job_id}, MD5: {md5_hash}")
        
        return JobResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
            created_at=job_data["created_at"],
            updated_at=job_data["created_at"]
        )
    
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", extra={"request_id": job_id})
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# Background task for dataset processing
async def process_dataset(job_id: str, df: pd.DataFrame, md5_hash: str):
    """Background task to train model on uploaded dataset"""
    try:
        # Update job status
        redis_client.setex(
            f"job:{job_id}",
            3600,
            json.dumps({"status": JobStatus.PROCESSING, "updated_at": datetime.utcnow()}, default=str)
        )
        
        # Train model
        trainer = SelfLearningTrainer()
        model, metrics = trainer.train_ensemble(df)
        
        # Evaluate model
        evaluator = ModelEvaluator()
        evaluation = evaluator.evaluate_model(model, df)
        
        # Save model to object store
        # TODO: Save to S3/GCS
        
        # Update job with results
        result = {
            "job_id": job_id,
            "status": JobStatus.COMPLETED,
            "md5_hash": md5_hash,
            "metrics": metrics,
            "evaluation": evaluation,
            "updated_at": datetime.utcnow()
        }
        
        redis_client.setex(f"job:{job_id}", 3600, json.dumps(result, default=str))
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as e:
        error_result = {
            "job_id": job_id,
            "status": JobStatus.FAILED,
            "error": str(e),
            "updated_at": datetime.utcnow()
        }
        redis_client.setex(f"job:{job_id}", 3600, json.dumps(error_result, default=str))
        logger.error(f"Job {job_id} failed: {str(e)}")

# Job Status Endpoint
@app.get("/api/v1/jobs/{job_id}", response_model=JobResponse, tags=["Jobs"])
async def get_job_status(job_id: str, api_key: str = Depends(verify_api_key)):
    """Get processing job status and results"""
    job_data = redis_client.get(f"job:{job_id}")
    
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_info = json.loads(job_data)
    
    return JobResponse(
        job_id=job_id,
        status=job_info.get("status"),
        created_at=job_info.get("created_at", datetime.utcnow()),
        updated_at=job_info.get("updated_at", datetime.utcnow()),
        result=job_info.get("metrics") if job_info.get("status") == JobStatus.COMPLETED else None,
        error=job_info.get("error")
    )

# Prediction Endpoint
@app.post("/api/v1/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_price(
    request: PredictionRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Generate price prediction for a property.
    Uses the latest trained model.
    """
    import uuid
    request_id = str(uuid.uuid4())
    
    try:
        # Load latest model from cache or storage
        # TODO: Implement model loading from object store
        
        # For now, use in-memory predictor
        predictor = RealEstatePredictor()
        
        # Prepare input data
        input_data = pd.DataFrame([{
            'area': request.area,
            'rooms': request.rooms,
            'bedrooms': request.bedrooms,
            'bathrooms': request.bathrooms,
            'parking spaces': request.parking_spots,
            'floor': request.floor,
            'animal': int(request.animal),
            'furniture': int(request.furniture),
            'city': request.city,
            'district': request.district or ''
        }])
        
        # Make prediction (placeholder)
        # TODO: Load actual model and predict
        predicted_price = 500000.0  # Placeholder
        
        # Calculate confidence interval
        confidence_interval = {
            "lower": predicted_price * 0.9,
            "upper": predicted_price * 1.1,
            "confidence_level": 0.95
        }
        
        # Find similar properties
        similar_properties = []  # TODO: Implement similarity search
        
        # Market insights
        market_insights = {
            "market_trend": "stable",
            "price_per_sqm": predicted_price / request.area,
            "location_multiplier": 1.0
        }
        
        logger.info(f"Prediction generated: {predicted_price}", extra={"request_id": request_id})
        
        return PredictionResponse(
            predicted_price=predicted_price,
            confidence_interval=confidence_interval,
            similar_properties=similar_properties,
            market_insights=market_insights,
            request_id=request_id
        )
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", extra={"request_id": request_id})
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# List Models Endpoint
@app.get("/api/v1/models", response_model=List[ModelInfo], tags=["Models"])
async def list_models(api_key: str = Depends(verify_api_key)):
    """List all available model versions with metrics"""
    # TODO: Query from database/object store
    models = [
        {
            "model_id": "oracle-v1",
            "version": "1.0.0",
            "md5_hash": "abc123def456",
            "metrics": {"mae": 50000, "r2": 0.85},
            "created_at": datetime.utcnow(),
            "is_active": True
        }
    ]
    return [ModelInfo(**m) for m in models]

# Feedback Endpoint
@app.post("/api/v1/feedback", tags=["Feedback"])
async def submit_feedback(
    feedback: FeedbackRequest,
    api_key: str = Depends(verify_api_key)
):
    """Submit user feedback for model improvement"""
    try:
        # Store feedback in database
        # TODO: Implement feedback storage
        
        # Trigger retraining if threshold met
        # TODO: Check if retraining needed
        
        logger.info(f"Feedback received for prediction {feedback.prediction_id}")
        
        return {
            "status": "success",
            "message": "Feedback received and will be used for model improvement"
        }
    except Exception as e:
        logger.error(f"Feedback submission failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Agent Chat Endpoint (for AI assistant)
@app.post("/api/v1/agent/chat", tags=["Agent"])
async def agent_chat(
    message: str,
    session_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Chat with Oracle Samuel AI Agent"""
    try:
        # Initialize agent
        agent = OracleSamuelAgent()
        
        # Get response
        response = agent.process_query(message)
        
        # Store chat history
        # TODO: Store in session management
        
        return {
            "response": response,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Agent chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        workers=int(os.getenv("WORKERS", 1)),
        log_config=None
    )

