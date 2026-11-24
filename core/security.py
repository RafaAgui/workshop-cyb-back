from datetime import datetime, timedelta
from jose import JWTError, jwt

# En producción esto va en una variable de entorno, NUNCA en el código
SECRET_KEY = "una-clave-secreta-muy-larga-y-dificil-de-adivinar"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    """Genera un JWT firmado con los datos que le pasemos"""
    to_encode = data.copy()

    # Le añadimos la fecha de expiración
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Lo firmamos con nuestra SECRET_KEY
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict | None:
    """Verifica que el token es válido y devuelve su contenido"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None