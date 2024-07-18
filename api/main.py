from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import root_routes, clock_routes
import threading
from utils import print_things, start_system
from clock import clock
import os
from storage import network_storage


list_hosts = [
    "http://localhost:5310",
    "http://localhost:8081",
    "http://localhost:8082",
    "http://localhost:8083"
]

list_hosts[0] = os.getenv('clock_1')
list_hosts[1] = os.getenv('clock_2')
list_hosts[2] = os.getenv('clock_3')
list_hosts[3] = os.getenv('clock_4')
id_clock = int(os.getenv('id_clock'))
network_storage.clocks["self_id"] = id_clock
network_storage.set_addrs(list_hosts)

print(id_clock)

if id_clock == 0:
    print("Papai, eu sou o lider")
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
clock.set_drift(0.9)
threading.Thread(target=clock.increment_time_background).start()
threading.Thread(target=clock.send_time).start()
