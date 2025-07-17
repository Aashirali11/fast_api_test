import jwt
from datetime import datetime, timedelta
from app.schemas import UserLogin, TokenData
from fastapi import HTTPException, status,Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app import db_models
from sqlalchemy.orm import Session


SECRET_KEY = "######"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


def create_access_token(data: dict, expires_delta: int = 30):
    data_to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expires_delta)
    data_to_encode.update({"exp": expire})
    jwt_token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:int = payload.get("user_id")
        print(type(id))
        if id is None:
            raise credentials_exception

        token_data =  TokenData(id=id)
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    return token_data

def get_current_user(token: str=Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token_data = verify_access_token(token, credentials_exception)

    user = db.query(db_models.User).filter(db_models.User.id == token_data.id).first()
    
    return user