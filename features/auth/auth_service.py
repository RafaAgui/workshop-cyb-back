from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simulamos una bbdd con un usuario de prueba
# En producción esto vendría de una base de datos real
FAKE_USERS_DB = {
    "user@example.com": {
        "username": "Jonh Doe",
        "email": "user@example.com",
        # Esto es "password123" hasheada. Nunca se guarda la contraseña en plano
        "hashed_password": pwd_context.hash("password123"),
    }
}

def get_user(email: str) -> dict | None:
    """Busca un usuario por email"""
    return FAKE_USERS_DB.get(email)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Comprueba que la contraseña introducida coincide con la hasheada"""
    return pwd_context.verify(plain_password, hashed_password)