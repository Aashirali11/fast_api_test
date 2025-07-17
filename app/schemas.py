from pydantic import BaseModel, Field,EmailStr
from datetime import datetime
from typing import Optional, List

class BaseSchemaModel(BaseModel):
    """
    Base schema model that can be extended by other models.
    It provides a common configuration for all schema models.
    """
    class Config:
        # This will allow the model to be used with ORM
        # orm_mode = True
        from_attributes = True

class PostBase(BaseSchemaModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    id:int = None  # Optional field for ID, can be used for creating new posts
    # This model is used for creating a new post
    # It inherits from PostBase and can be extended with additional fields if needed
    pass
class PostGetList(BaseSchemaModel):
    # This model is used for creating a new post
    # It inherits from PostBase and can be extended with additional fields if needed
    data :List[PostBase]

class PostUpdate(PostBase):
    # This model is used for updating an existing post
    # It inherits from PostBase and can be extended with additional fields if needed
    pass


class UserBase(BaseSchemaModel):
    email: EmailStr
        
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

class UserLogin(BaseSchemaModel):
    email: EmailStr = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")

class Token(BaseSchemaModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseSchemaModel):
    id: Optional[int] = None