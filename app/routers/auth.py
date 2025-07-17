from app import db_models, schemas, oauth2
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils import *
router = APIRouter(
    tags=["Auth"],
    prefix="/api/v1"
)

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(payload: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.email == payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", status_code=status.HTTP_200_OK)
def login_user(payload: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.email == payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED, detail="User not found")
    
    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"token": access_token, "token_type": "bearer"}