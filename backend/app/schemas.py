from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- User Schemas ---

# Properties required when creating a user.
class UserCreate(BaseModel):
    email: EmailStr
    name: str | None = None

# Properties to return to the client.
# We don't want to return the password, for example.
class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str | None
    created_at: datetime

    # This tells Pydantic to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes).
    class Config:
        orm_mode = True