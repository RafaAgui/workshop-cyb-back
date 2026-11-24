from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Se importa

from features.auth.auth_router import router as auth_router
from features.protected.protected_router import router as protected_router  # NUEVO


app = FastAPI()

# Se incluye

app.include_router(auth_router)
app.include_router(protected_router)  # NUEVO

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:4201"], # solo Angular
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
  )