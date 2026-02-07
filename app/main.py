from fastapi import FastAPI

# Database
from app.database.db import engine, Base

# Models (so tables are created)
from app.models.prediction import Prediction
from app.models.user import User

# Routers
from app.routes.predict import router as predict_router
from app.routes.auth import router as auth_router

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app FIRST
app = FastAPI(
    title="SpaceAI API",
    version="1.0"
)

# Include routers AFTER app is defined
app.include_router(predict_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "SpaceAI Backend Running 🚀"}

