from app import db_models, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils import *
router = APIRouter(
    tags=["Auth"],
    prefix="/api/v1"
)

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return {"token": "fake-jwt-token"}