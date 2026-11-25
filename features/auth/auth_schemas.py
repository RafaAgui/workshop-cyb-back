from pydantic import BaseModel

# Lo que nos envía Angular en el body del POST
class LoginRequest(BaseModel):
    email: str
    password: str
class UserResponse(BaseModel):
    username: str
    email: str