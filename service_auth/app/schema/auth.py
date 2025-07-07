from pydantic import BaseModel, EmailStr

class UserSignin(BaseModel):
    email: EmailStr
    password: str

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int

class RefreshTokenRequest(BaseModel):
    refresh_token: str