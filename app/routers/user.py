from app import db_models, schemas
from app.database import get_db
from app.utils import hash_password
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Users"],
    prefix="/api/v1"
)

@router.post("/users",response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
def create_new_posts(payload:schemas.UserCreate,db:Session = Depends(get_db)):
    users = db_models.User(**payload.model_dump())
    # Hash the password before storing it
    hash_pwd = hash_password(users.password)
    users.password = hash_pwd
    
    db.add(users)
    try:
        db.commit()
        db.refresh(users)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    # return {"usercreated":users}
    return users


@router.get("/users/{id}",response_model=schemas.UserResponse)
def get_user_by_id(id:int,db:Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with this id:{id} not found")
    return user