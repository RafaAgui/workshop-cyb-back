from fastapi import APIRouter, Depends, HTTPException, Response, status
from core.config import settings
from core.dependencies import get_current_user
from features.auth.auth_schemas import LoginRequest, UserResponse
from features.auth.auth_service import get_user, verify_password
from core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
COOKIE_NAME = "access_token"


@router.post("/login", response_model=UserResponse)
def login(credentials: LoginRequest, response: Response):
    user = get_user(credentials.email)

    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    token = create_access_token(data={
        "sub": user["email"],
        "username": user["username"],
    })

    # El token viaja en una cookie, no en el body
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,                       # JavaScript no puede leerla
        secure=settings.COOKIE_SECURE,       # solo HTTPS en producción
        samesite="lax",                      # no se envía en peticiones cross-site
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )

    return UserResponse(username=user["username"], email=user["email"])


@router.post("/logout")
def logout(response: Response):
    # Ahora el logout SÍ lo hace el back: borra la cookie.
    # Los parámetros deben coincidir con los del set_cookie.
    response.delete_cookie(
        key=COOKIE_NAME,
        path="/",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
    )
    return {"mensaje": "Logout correcto"}


@router.get("/me", response_model=UserResponse)
def me(current_user: dict = Depends(get_current_user)):
    """Sirve para restaurar la sesión al recargar la página."""
    return UserResponse(
        username=current_user["username"],
        email=current_user["sub"],
    )