from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database.deps import get_db
from app.services.security import verify_password
from app.services.jwt import create_access_token
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        return {"error": "Invalid credentials"}

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}
