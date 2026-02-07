from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.database.db import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    # ✅ Link prediction to user
    user_id = Column(Integer, ForeignKey("users.id"))

    filename = Column(String)
    label = Column(String)
    confidence = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

