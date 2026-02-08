from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import engine, Base
from app.models.user import User
from app.models.prediction import Prediction

from app.routes.predict import router as predict_router
from app.routes.auth import router as auth_router


app = FastAPI(title="SpaceAI API", version="1.0")


# ✅ CORS Fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Create Tables on Startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# ✅ Routers
app.include_router(auth_router)
app.include_router(predict_router)


@app.get("/")
def home():
    return {"message": "SpaceAI Backend Running 🚀"}
