from pydantic import BaseModel

# Lo que nos envía Angular en el body del POST
class LoginRequest(BaseModel):
    email: str
    password: str

# Lo que le devolvemos a Angular
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    email: str