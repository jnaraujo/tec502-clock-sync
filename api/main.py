from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import root_routes, clock_routes
import threading
from clock import clock
import os
from storage import network_storage
import random

network_storage.add_addr(os.getenv('clock_1'))
network_storage.add_addr(os.getenv('clock_2'))
network_storage.add_addr(os.getenv('clock_3'))
network_storage.add_addr(os.getenv('clock_4'))

id_clock = int(os.getenv('id_clock'))
network_storage.clocks["self_id"] = id_clock

if id_clock == 0:
    network_storage.set_leader(id_clock)

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
clock.set_drift(random.uniform(0.7, 1.3))
threading.Thread(target=clock.increment_time_background, daemon=True).start()
threading.Thread(target=clock.send_time, daemon=True).start()