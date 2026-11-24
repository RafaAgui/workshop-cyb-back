from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import verify_token

# Le dice a FastAPI que espere un token Bearer en la cabecera Authorization
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """
    Dependencia reutilizable. Se inyecta en cualquier endpoint que queramos proteger.
    Extrae el token, lo verifica y devuelve el payload si es válido.
    """

    token = credentials.credentials

    # Verificamos el token usando la función que creamos ayer
    payload = verify_token(token)

    # Si verify_token devuelve None, el token es inválido o ha expirado
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload