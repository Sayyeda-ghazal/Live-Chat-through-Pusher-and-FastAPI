from fastapi import Form
from pydantic import BaseModel

class users(BaseModel):
    username: str = Form(...),
    message: str = Form(...)