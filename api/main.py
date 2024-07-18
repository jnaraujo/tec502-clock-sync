from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import root_routes, clock_routes
import threading
from utils import print_things, start_system
from clock import clock

app = FastAPI()

# Adiciona o middleware para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define as rotas
app.include_router(root_routes.router)
app.include_router(clock_routes.router)

# Inicia o relógio
clock.set_drift(0.9)
Thread(target=clock.increment_time_background).start()
