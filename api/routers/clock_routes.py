from fastapi import APIRouter, HTTPException
from clock import clock
from storage import clock_storage

router = APIRouter()


@router.get("/time", status_code=200)
def get_local_time():
  return {"time": clock.get_time()}

@router.post("/time", status_code=200)
def set_local_time(new_time: int):
  # se o tempo enviado pelo cliente for menor que o tempo atual
  # o banco atual deve ser o novo leader
  if new_time < clock.get_time():
    # TODO: definir o banco atual como novo leader e enviar a mensagem para os outros relógios
    raise HTTPException(status_code=400, detail="New time is less than current time")
  
  clock.set_time(new_time)
  return {"time": clock.get_time()}


@router.get("/shift", status_code=200)
def get_shift():
  return {"shift": clock.get_shift()}

@router.get("/leader", status_code=200)
def get_leader():
  addr = clock_storage.get_leader_addr()
  return {"leader": addr}