from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    pass # In this case, it's the same as UserBase

# Properties to return to client
class UserOut(UserBase):
    id: int
    created_at: datetime

    # This tells the Pydantic model to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes).
    model_config = ConfigDict(from_attributes=True)