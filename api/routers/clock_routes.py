from fastapi import APIRouter, HTTPException
from clock import clock
from storage import network_storage

router = APIRouter()

@router.post("/time/{new_time}/{id_leader}/{time_sync}", status_code=200)
def set_local_time(new_time: int, id_leader: int, time_sync: int):
  # se o tempo enviado pelo cliente for menor que o tempo atual
  # o banco atual deve ser o novo leader
  if new_time < clock.get_time():
    network_storage.set_leader(network_storage.get_self_id())
    raise HTTPException(status_code=403, detail="New time is less than current time")
  
  # atualiza o tempo do relógio
  clock.set_update_time()
  # atualiza o novo líder
  network_storage.set_leader(id_leader)
  # define o novo tempo
  clock.set_time(new_time)
  #define para sincronização
  clock.set_time_sync(time_sync)
  return {"time": clock.get_time()}

@router.post("/internal/time/{new_time}", status_code=200)
def set_internal_time(new_time: int):
  if(new_time < clock.get_time()):
    raise HTTPException(status_code=403, detail="New time is less than current time")
  clock.set_time(new_time)
  return {"time": clock.get_time()}

@router.get("/clock", status_code=200)
def get_clock():
  return {
    'time': clock.get_time(),
    'is_leader':  network_storage.is_self_leader(),
    'self_id': network_storage.get_self_id(),
    'leader_id': network_storage.get_leader(),
    'drift': clock.get_drift(),
    'time_sync': clock.get_time_sync()
  }

@router.get("/drift", status_code=200)
def get_drift():
  return {"drift": clock.get_drift()}


@router.post("/drift/{new_drift}", status_code=200)
def set_drift(new_drift: float):
  if new_drift <= 0:
    raise HTTPException(status_code=403, detail="Drift must be greater than 0")
  clock.set_drift(new_drift)

@router.get('/time-sync', status_code=200)
def get_time_to_sync():
  return {"time_sync": clock.get_time_sync()}

@router.post('/time-sync/{new_time}', status_code=200)
def set_new_time_to_sync(new_time: int):
  if(new_time < 1 or new_time > 10):
    raise HTTPException(status_code=403, detail="Time to sync must be greater than 1 or under 10")
  clock.set_time_sync(new_time)