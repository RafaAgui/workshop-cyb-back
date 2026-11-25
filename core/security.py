from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from core.config import settings

def create_access_token(data: dict) -> str:
    """Genera un JWT firmado con los datos que le pasemos"""
    to_encode = data.copy()

    # Le añadimos la fecha de expiración
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Lo firmamos con nuestra SECRET_KEY
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> dict | None:
    """Verifica que el token es válido y devuelve su contenido"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None