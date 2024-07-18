from fastapi import APIRouter, HTTPException
from clock import clock
from storage import network_storage

router = APIRouter()

@router.get("/time", status_code=200)
def get_local_time():
  return {"time": clock.get_time()}

@router.post("/time/{new_time}/{id_leader}", status_code=200)
def set_local_time(new_time: int, id_leader: int):
  # se o tempo enviado pelo cliente for menor que o tempo atual
  # o banco atual deve ser o novo leader
  if new_time < clock.get_time():
    network_storage.set_leader(network_storage.get_self_id())
    raise HTTPException(status_code=403, detail="New time is less than current time")
  
  network_storage.set_leader(id_leader)
  clock.set_time(new_time)
  return {"time": clock.get_time()}

@router.get("/clock", status_code=200)
def get_clock():
  return {
    'time': clock.get_time(),
    'is_leader':  network_storage.is_self_leader(),
    'self_id': network_storage.get_self_id(),
    'leader_id': network_storage.get_leader(),
    'drift': clock.get_drift()
  }

@router.get("/drift", status_code=200)
def get_drift():
  return {"drift": clock.get_drift()}


@router.post("/drift/{new_drift}", status_code=200)
def set_drift(new_drift: float):
  clock.set_drift(new_drift)


@router.get("/leader", status_code=200)
def get_leader():
  return {
    "leader": network_storage.get_leader_addr(), 
    "id_leader": network_storage.get_leader()
  }