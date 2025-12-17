from pydantic import BaseModel, EmailStr


class Question(BaseModel):
    question: str


class Prospect(BaseModel):
    name: str
    email: EmailStr
    message: str
