from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str
    pseudo: str
    age: int
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    pseudo: str
    age: int

    class Config:
        orm_mode = True
