from fastapi import APIRouter, Depends
from core.dependencies import get_current_user

router = APIRouter(prefix="/protected", tags=["protected"])

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """
    Solo accesible con un JWT válido.
    Devuelve los datos del usuario extraídos del token.
    """
    return {
        "mensaje": "Acceso concedido",
        "username": current_user.get("username"),
        "email": current_user.get("sub"),
    }


@router.get("/data")
def get_protected_data(current_user: dict = Depends(get_current_user)):
    """
    Otro endpoint protegido de ejemplo.
    El Depends(get_current_user) es todo lo que necesitamos para protegerlo.
    """
    return {
        "mensaje": f"Hola {current_user.get('username')}, estos son tus datos secretos",
        "data": ["dato_1", "dato_2", "dato_3"],
    }