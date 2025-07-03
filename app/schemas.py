from pydantic import BaseModel, Field,EmailStr
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

class UserCreateResponse(BaseSchemaModel):
    usercreated: UserBase