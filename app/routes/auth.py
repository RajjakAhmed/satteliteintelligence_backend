from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database.deps import get_db
from app.services.security import verify_password, hash_password
from app.services.jwt import create_access_token
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter(prefix="/api/auth", tags=["Auth"])


# -------------------------------
# ✅ REGISTER
# -------------------------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# -------------------------------
# ✅ LOGIN (OAuth2 Form)
# -------------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}
