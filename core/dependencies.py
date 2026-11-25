from fastapi import Cookie, HTTPException, status
from core.security import verify_token


def get_current_user(access_token: str | None = Cookie(default=None)) -> dict:
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
        )

    payload = verify_token(access_token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    return payload