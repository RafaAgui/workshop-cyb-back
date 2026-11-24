from fastapi import APIRouter, HTTPException, status
from features.auth.auth_schemas import LoginRequest, TokenResponse
from features.auth.auth_service import get_user, verify_password
from core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):

    # 1. Buscamos el usuario en la bbdd
    user = get_user(credentials.email)

    # 2. Comprobamos que existe Y que la contraseña es correcta
    # OJO: un solo mensaje de error, sin pistas de qué ha fallado
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    # 3. Generamos el JWT con los datos del usuario en el payload
    token = create_access_token(data={
        "sub": user["email"],
        "username": user["username"],
    })

    # 4. Lo devolvemos
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        username=user["username"],
        email=user["email"],
    )


@router.post("/logout")
def logout():
    # El logout real se gestiona en el frontend borrando el token
    # El backend no guarda tokens, así que no tiene nada que borrar
    return {"mensaje": "Logout correcto"}