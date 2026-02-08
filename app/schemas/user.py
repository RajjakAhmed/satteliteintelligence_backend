from pydantic import BaseModel, EmailStr


# -------------------------
# Register Schema
# -------------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# -------------------------
# Login Schema
# -------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str
