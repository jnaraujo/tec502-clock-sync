from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import root_routes
import threading
from utils import print_things, start_system

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_routes.router)


threading.Thread(target=start_system).start()