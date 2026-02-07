from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.services.auth import get_current_user

from app.models.user import User
from app.models.prediction import Prediction

from app.services.storage import upload_image_to_supabase
from app.ml.hf_client import predict_from_huggingface

router = APIRouter(prefix="/api", tags=["Prediction"])


# ✅ POST Prediction
@router.post("/predict")
async def predict_land(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user),
):
    # Validate image
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Only JPG/PNG allowed")

    # Get logged-in user
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Upload image → Supabase public URL
    image_url = upload_image_to_supabase(file)

    # ✅ HuggingFace Prediction
    label, confidence = predict_from_huggingface(image_url)

    # ✅ Save prediction
    new_pred = Prediction(
        user_id=user.id,
        filename=file.filename,
        label=label,
        confidence=confidence,
    )

    db.add(new_pred)
    db.commit()
    db.refresh(new_pred)

    # ✅ Keep only last 10 predictions
    preds = (
        db.query(Prediction)
        .filter(Prediction.user_id == user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )

    if len(preds) > 10:
        for old in preds[10:]:
            db.delete(old)
        db.commit()

    return {
        "label": label,
        "confidence": confidence,
        "image_url": image_url,
        "message": "Prediction stored successfully (last 10 only)"
    }


# ✅ GET History
@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user),
):
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    history = (
        db.query(Prediction)
        .filter(Prediction.user_id == user.id)
        .order_by(Prediction.created_at.desc())
        .limit(10)
        .all()
    )

    return history
