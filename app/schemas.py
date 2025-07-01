from pydantic import BaseModel, Field

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    id:int = None  # Optional field for ID, can be used for creating new posts
    # This model is used for creating a new post
    # It inherits from PostBase and can be extended with additional fields if needed
    pass
class PostUpdate(PostBase):
    # This model is used for updating an existing post
    # It inherits from PostBase and can be extended with additional fields if needed
    pass
