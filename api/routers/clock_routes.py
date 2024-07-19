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
  elif(new_time > clock.get_time()):
    network_storage.set_leader(id_leader)
    clock.set_time(new_time)
    clock.set_counter_timeout(0)
    clock.set_received_time_by_leader(True)
    return {"time": clock.get_time()}

@router.post("/internal/time/{new_time}", status_code=200)
def set_internal_time(new_time: int):
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

@router.post('/leader-sync-make', status_code=200)
def await_leader():
  clock.set_is_sync(True)


@router.post('/leader-sync-complete', status_code=200)
def return_increment():
  clock.set_is_sync(False)


@router.get('/time-sync', status_code=200)
def get_time_sync_leader():
  return {
    'time-sync': clock.get_time_to_sync(),
    'is_leader': network_storage.is_self_leader()
    }


@router.post('/time-sync/{new_time_sync}', status_code=200)
def set_new_time_to_sync(new_time_sync):
  if(not network_storage.is_self_leader()):
    raise HTTPException(status_code=406, detail="Clock not leader, update time-sync not possible")
  if(new_time_sync >5):
    raise HTTPException(status_code=406, detail="Time to sync is too long")
  clock.set_time_to_sync(new_time_sync)
  
@router.get('/time-out', status_code=200)
def get_timeout_counter():
  return {'time_now': clock.get_counter_timeout()}